# online-latex-mathmatical-fomula

## 介绍
为了解决 [GitHub 支持 LaTex 的几种方案以及 LaTeX 生成 svg](https://github.com/Hzzone/Hzzone.github.io/issues/7)，我最后还是自己实现了一个在线 Latex 数学编辑。

支持的功能和原理如下:
* 实时预览: [MathJax](https://www.mathjax.org/) 实时渲染公式
* 导出 gif/png/svg 和外链: 保存在本地 nginx/images，并使用 [clipboard.js](https://clipboardjs.com/) 自动粘贴。
* 使用 [codecogs](http://www.codecogs.com/latex/eqneditor.php) API，但是保存本地目录。
* 自动补全和高亮: [Ace Editor](https://ace.c9.io/) 的 LaTeX 模式和 chrome 主题。

## 使用
在线预览: [demo](https://hzzone.io/api/latex)

可以研究一下代码，非常简单，只需要改几个链接就可以架设到自己的服务器上。