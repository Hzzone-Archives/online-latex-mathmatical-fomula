from flask import Flask, request, Response, render_template
from urllib.parse import unquote
import requests
import os
import base64
import json

app = Flask(__name__)
IMAGE_DIR = '/usr/share/nginx/html/images'
# IMAGE_DIR = 'images'

def save_img(codecogs_url, image_path):
    r = requests.get(codecogs_url)
    with open(image_path, 'wb') as f:
        f.write(r.content)

@app.route('/api/latex')
def index():
    return render_template('index.html')


@app.route('/api/latex/<type>')
def getLaTexImage(type):
    type = unquote(type, 'utf-8')
    return_result = {'success': True}
    expression = request.args.get('expression')
    if not expression:
        return_result['success'] = False
        return json.dumps(return_result)

    print(return_result)
    expression = expression.replace('$', '')
    codecogs_url = 'http://latex.codecogs.com/{}.latex?{}'.format(type, expression)
    expression_bs64 = base64.b64encode(expression.encode()).decode()
    image_path = '{}/{}.{}'.format(IMAGE_DIR, expression_bs64, type)
    if not os.path.exists(image_path):
        save_img(codecogs_url, image_path)

    return json.dumps(return_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)