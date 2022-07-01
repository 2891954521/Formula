from flask import Flask, request

import Core

app = Flask(__name__)


@app.route('/upload', methods = ['POST'])
def upload():
    image = request.files.get("image").read()

    if image is None:
        return {
            'code': 500,
            'msg': '文件上传为空',
            'formula': '',
            'result': ''
        }
    else:
        formula, result = Core.process(image)
        return {
            'code': 200,
            'msg': '文件上传成功',
            'formula': formula,
            'result': result
        }


def run():
    app.run(host='0.0.0.0', port=8080, debug=False)