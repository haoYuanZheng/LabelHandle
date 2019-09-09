from flask import Flask, request, render_template, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from flask_cors import *
import os
import json

app = Flask(__name__)
CORS(app)
# 最大文件限制目前为3M
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
# 上传文件允许类型
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
# 存储地址
app.config['UPLOAD_FOLDER'] = 'static/uploads/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # 多文件上传先遍历
        for file in request.files.getlist('file'):
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "images/", filename))
                # 当为post请求时保存文件并刷新页面
            else:
                return jsonify({"error": 1001, "msg": "请检查上传的图片类型，仅限于png、jpg、jpeg、gif"})
        return redirect(url_for('upload'))
    else:
        return render_template('index.html')


@app.route("/view", methods=['POST'])
def view():
    # 项目系统目录，防止放入镜像时路径错误
    rootdir = app.root_path + "/static/uploads/images"
    picutres = {}
    for filenames in os.walk(rootdir):
        if filenames is not None:
            names = filenames[2]
            break
    if names is not None:
        for name in names:
            picutres[name] = "static/uploads/images/" + name
    return json.dumps(picutres)


# 因跨域问题，先模拟图片加工接口
@app.route("/getImageTest", methods=['POST'])
def getImageTest():
    return json.dumps("00006_LLGJ65.jpg")


if __name__ == '__main__':
    app.run()
