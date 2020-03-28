#!/usr/bin/env python
# encoding: utf-8
"""
@author: yangwei.1024
@file: app.py
@time: 2020-03-28 17:33
@desc: flask实现后端/前端页面
"""

from flask import Flask, request, render_template, redirect, url_for, flash, render_template_string
from requests import Session
import logging
import json
import os
import uuid
from flask import send_from_directory
from flask_cors import *
from flask import send_file, send_from_directory
import os
from flask import make_response
from AliIMG import *

logging.basicConfig(level="INFO")

app = Flask(__name__,
            static_url_path="/",
            template_folder="templates",
            static_folder="static")

CORS(app, supports_credentials=True)


# 工具导航
@app.route("/")
def allCaseMaker():
    return render_template("1688Download.html", context={})


# 下载图片
@app.route("/download", methods=["POST"])
def case_export_all():
    if request.method == 'POST':
        # 从表单读传入的数据
        url = request.form.get('url')
        crawle(url)
        res = "下载成功"
        return render_template('1688DownloadRes.html', context={}, res=res)
    else:
        return render_template('1688Download.html', context={})


if __name__ == '__main__':
    app.run(host="0.0.0.0",
            port=5000,
            debug=True)
