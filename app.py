from flask import Flask, request, Response, render_template
from urllib.parse import unquote
import json

import config

app = Flask(__name__, static_url_path='/api/static')
# app = Flask(__name__, static_url_path='/static')
# app = Flask(__name__)


@app.route('/api/latex')
def index():
    return render_template('index.html')


@app.route('/api/md')
def markdown():
    return render_template('markdown.html')


@app.route('/api/latex/<image_type>')
def getLaTexImage(image_type):
    image_type = unquote(image_type, 'utf-8')
    return_result = {'success': True}
    expression = request.args.get('expression')
    if not expression:
        return_result['success'] = False
        return json.dumps(return_result)

    expression = expression.replace('$', '')

    return_result['success'] = config.generate_ways[config.generate_way](expression, image_type, config.IMAGE_DIR)

    return json.dumps(return_result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1111, debug=True)
