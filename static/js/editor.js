// config
// 生成的图片链接地址
base_url = "https://tuchuang-1252747889.cos.ap-guangzhou.myqcloud.com/expression/";

// 最长的公式长度
var max_formula_length = 200;

toastr.options.positionClass = 'toast-top-full-width';
toastr.options.extendedTimeOut = 0; //1000;
toastr.options.timeOut = 1000;
toastr.options.fadeOut = 250;
toastr.options.fadeIn = 250;

// 换行公式模板，可在此添加样式
var newline_formula_template = '\n<div align="center"><img alt="{0}" src="{1}{2}.{3}" /></div>\n';

// inline 公式
var inline_formula_template = '![{0}]({1}{2}.{3})';

// image_type gif/svg/png
var image_type = "svg";

// 编辑器字体大小
var editor_font_size = "16px";

// 行内公式 图片宽度
var inline_image_width = "16px";

// 排除有中文的公式
function has_chinese(text) {
    return /.\*[/u4e00\ - /u9fa5]\+.\*$/g.test(text);
}

// window.btoa 中文报错
Base64 = {
    encode: function(str) {
        // first we use encodeURIComponent to get percent-encoded UTF-8,
        // then we convert the percent encodings into raw bytes which
        // can be fed into btoa.
        return btoa(encodeURIComponent(str).replace(/%([0-9A-F]{2})/g,
        function toSolidBytes(match, p1) {
            return String.fromCharCode('0x' + p1);
        }));
    },
    decode: function(str) {
        // Going backwards: from bytestream, to percent-encoding, to original string.
        return decodeURIComponent(atob(str).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice( - 2);
        }).join(''));
    }
};

function Toast(type, css, msg) {
    this.type = type;
    this.css = css;
    this.msg = msg;
}

// 格式化字符串
String.prototype.format = function() {
    var formatted = this;
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{' + i + '\\}', 'gi');
        formatted = formatted.replace(regexp, arguments[i]);
    }
    return formatted;
};

function upload_to_server(expression, type) {
    // var success = true;
    $.ajax({
        type: 'GET',
        url: "latex/{0}".format(type),
        // async: false,
        data: {
            "expression": expression
        },
        success: function(result) {
            console.log(result);
            result = $.parseJSON(result);
            if (result['success']) {
                // showToast(3);
            } else {
                showToast('error', 'toast-top-center', '部分公式生成失败，请检查一下美元符是否对齐');
                success = false;
            }
        },
        error: function() {
            showToast('error', 'toast-top-center', '服务器请求失败，可能没网或者服务器挂了');
        }
    });
    // return success;
}

function save_local(expression, type) {
    var success = true;

    return success;
}

function replace(content, regx, base_url, template, type, is_upload) {

    // 贪婪匹配会匹配到重复的
    // 多行 $$\nformula\n$$ 匹配 http://www.kkh86.com/it/regexp/guide-base-multiple-line.html
    // 如果美元符不匹配，一般中文都会匹配，会有500报错...没办法解决，只能限制expression.length的长度了
    // regx: /\$\$([\s\S]*?)\$\$/gm
    content = content.replace(regx,
    function(result) {
        var expression = result.replace(/\$/g, "");
        expression = expression.replace(/\n/g, '');
        if (!is_upload) {
            // 本地显示处理 latex 转义字符
            expression = expression.replace(/\\\\/g, '\\\\\\\\');
            expression = expression.replace(/\\ /g, '\\\\ ');
            expression = expression.replace(/\\%/g, '\\\\%');
            expression = expression.replace(/\\{/g, '\\\\{');
            expression = expression.replace(/\\}/g, '\\\\}');
            expression = expression.replace(/\\#/g, '\\\\#');
            expression = expression.replace(/\\~/g, '\\\\~');
            expression = expression.replace(/\\_/g, '\\\\_');
            expression = expression.replace(/\\&/g, '\\\\&');
            expression = expression.replace(/\\\$/g, '\\\\$');
            expression = expression.replace(/\\\^/g, '\\\\^');

            var dollar_length = result.match(/\$/ig).length;
            if(dollar_length==2)
                expression = '$'+expression+'$';
            else if(dollar_length==4)
                expression = '$$'+expression+'$$';
            else
                showToast('error', 'toast-top-center', '美元符未对齐');
            return expression;
        }
        console.log(expression);
        // 如果$$匹配长度超过限制则不替换
        if (expression.length > max_formula_length || has_chinese(expression)) return result;
        upload_to_server(expression, type);
        var encodedData = Base64.encode(expression);
        // '\n<div align="center"><img src="https://hzzone.io/images/' + encodedData + '.gif" /></div>\n';
        // '\n<div align="center"><img src="{0}/{1}.{2}" /></div>\n';
        return template.format(expression, base_url, encodedData, type);
    });
    return content;

}

function showToast(type, position, content) {
    var toast = new Toast(type, position, content);
    toastr.options.positionClass = toast.css;
    toastr[toast.type](toast.msg);
}

var editor = ace.edit("author-editor", {
    theme: "ace/theme/chrome",
    mode: "ace/mode/markdown",
    wrap: true,
    autoScrollEditorIntoView: true,
    minLines: 2
});

$("#editor").css("font-size", editor_font_size);

editor.session.on('change',
function(delta) {
    var content = editor.getValue();
    content = replace(content, /\$\$([\s\S]*?)\$\$/gm, '', '', '', false);
    content = replace(content, /\$([\s\S]*?)\$/gm, '', '', '', false);
    $(".result_html").html(marked(content));
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, "result_content"]);
});

$(function() {
    $("[data-toggle='tooltip']").tooltip();
});

$('#download_button').click(function() {
    $("#download_button").attr("disabled","disabled");
    var content = editor.getValue();

    content = replace(content, /\$\$([\s\S]*?)\$\$/gm, base_url, newline_formula_template, image_type, true);
    content = replace(content, /\$([\s\S]*?)\$/gm, base_url, inline_formula_template, image_type, true);

    $("#download_button").removeAttr("disabled");
    var clipboard = new ClipboardJS('#download_button', {
        text: function(trigger) {
            //剪切板内容
            return content;
        }
    });
    clipboard.on('success',
    function(e) {
        showToast('success', 'toast-top-center', '复制成功');
        e.clearSelection();
        clipboard.destroy();
    });

    clipboard.on('error',
    function(e) {
        console.log(e);
        showToast('error', 'toast-top-center', 'Clipboard 复制失败');
        clipboard.destroy();
    });
});