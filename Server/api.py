from flask import Flask, request

import Core

app = Flask(__name__)


@app.route('/upload', methods = ['POST'])
def upload():
    image = request.files.get("image").read()

    if image is None:
        return {
            'code': 500,
            'msg': '文件上传为空'
        }
    else:
        return {
            'code': 200,
            'msg': Core.process(image)
        }


def run():
    app.run()