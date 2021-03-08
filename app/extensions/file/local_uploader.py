import os
import re
from flask import current_app
from werkzeug.utils import secure_filename

from lin.core import File
from lin.file import Uploader


class LocalUploader(Uploader):

    def upload(self,type):
        ret = []
        current_path=current_app.static_url_path
        # 创建文件夹
        self.mkdir_if_not_exists(type)
        site_domain = current_app.config.get('SITE_DOMAIN')\
            if current_app.config.get('SITE_DOMAIN') else 'http://127.0.0.1:2100'
        for single in self._file_storage:
            file_md5 = self._generate_md5(single.read())
            single.seek(0)
            exists = File.query.filter_by(md5=file_md5).first()
            if exists:
                ret.append({
                    "key": single.name,
                    "id": exists.id,
                    "title": exists.title,
                    "path": exists.path,
                    "url":  os.path.join(site_domain+current_path, exists.path)
                })
            else:
                # 获取文件夹
                absolute_path, relative_path, real_name = self._get_store_path(single.filename)
                secure_filename(single.filename)
                file_title=single.filename
                single.save(absolute_path)
                file = File.create_file(
                    type=type,
                    name=real_name,
                    title=file_title,
                    path=os.path.join('/'+type,relative_path),
                    extension=self._get_ext(single.filename),
                    size=self._get_size(single),
                    md5=file_md5,
                    commit=True
                )
                ret.append({
                    "key": single.name,
                    "id": file.id,
                    "title": file.title,
                    "path": file.path,
                    "url": os.path.join(site_domain+current_path, file.path)
                })
        return ret
