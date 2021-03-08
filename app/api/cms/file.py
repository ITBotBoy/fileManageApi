"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from lin.exception import ParameterException
from flask import request, jsonify,current_app
from lin import login_required
from lin.redprint import Redprint
from app.validators.files import FileType
from app.extensions.file.config import FILE
from app.extensions.file.local_uploader import LocalUploader

file_api = Redprint('file')
typeRadio=('img','txt','video','audio')

@file_api.route('', methods=['POST'])
@login_required
def post_file():
    files = request.files
    type=request.form.get("type")
    if not type or type not in typeRadio:
       raise ParameterException(msg={type: ["Not a valid choice"]})
    config = FILE[type]
    uploader = LocalUploader(files,config)
    ret = uploader.upload(type)
    return jsonify(ret)
