import requests
import base64
import subprocess
import os
import cairosvg
import logging

def codecogs(expression, image_type, IMAGE_DIR):
    expression_bs64 = base64.b64encode(expression.encode()).decode()
    image_path = '{}/{}.{}'.format(IMAGE_DIR, expression_bs64, image_type)
    if not os.path.exists(image_path):
        codecogs_url = 'http://latex.codecogs.com/{}.latex?{}'.format(image_type, expression)
        try:
            r = requests.get(codecogs_url)
        except requests.exceptions.Timeout:
            return False
        with open(image_path, 'wb') as f:
            f.write(r.content)
    return True

def tex2svg(expression, image_type, IMAGE_DIR):
    expression_bs64 = base64.b64encode(expression.encode()).decode()
    svg_image_path = '{}/{}.{}'.format(IMAGE_DIR, expression_bs64, 'svg')
    image_path = '{}/{}.{}'.format(IMAGE_DIR, expression_bs64, image_type)
    if not os.path.exists(image_path):
        command = '''tex2svg '{}' > {}'''.format(expression, svg_image_path)
        shell_return = subprocess.call(command, shell=True, stdout=open('generate.log', 'w'))
        # shell_return == 0 if success
        if shell_return:
            return False
        if image_path == svg_image_path:
            cairosvg.svg2png(url=svg_image_path, write_to=image_path)
    return True

def dvisvgm(expression, image_type, IMAGE_DIR):
    print(expression)
    expression_bs64 = base64.b64encode(expression.encode()).decode()
    svg_image_path = '{}/{}.{}'.format(IMAGE_DIR, expression_bs64, 'svg')
    image_path = '{}/{}.{}'.format(IMAGE_DIR, expression_bs64, image_type)
    if not os.path.exists(image_path):
        latex_content = r'''
        \documentclass[paper=a5,fontsize=15px]{scrbook}
        \usepackage[pdftex,active,tightpage]{preview}
        \usepackage{amsmath}
        \usepackage{amssymb}
        \usepackage{amsfonts}
        \usepackage{tikz}
        \begin{document}
        \begin{preview}
        \begin{tikzpicture}[inner sep=0pt, outer sep=0pt]
        \node at (0, 0) {\begin{math} 
        ''' \
        + expression + \
        r'''
        \end{math}}; % <--Put your tex-code here
        \end{tikzpicture}
        \end{preview}
        \end{document}
        '''

        with open('/tmp/{}.tex'.format(expression_bs64), 'w') as f:
            f.write(latex_content)
        command1 = 'latex -output-directory /tmp /tmp/{}.tex '.format(expression_bs64)
        command2 = 'dvisvgm --no-fonts /tmp/{}.dvi -o {}'.format(expression_bs64, svg_image_path)

        shell_return = subprocess.call(command1, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
        if shell_return:
            return False
        shell_return = subprocess.call(command2, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
        if shell_return:
            return False
        if not image_path == svg_image_path:
            cairosvg.svg2png(url=svg_image_path, write_to=image_path)
    return True


