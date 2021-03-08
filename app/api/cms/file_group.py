from flask import jsonify,request
from lin import route_meta, group_required, login_required
from lin.exception import Success,Forbidden,NotFound
from lin.redprint import Redprint
from lin import db
import math
from app.models.file_group import FileGroup
from app.models.group_img import ImgGroup
from app.models.group_video import VideoGroup
from app.models.group_txt import TxtGroup
from app.models.group_audio import AudioGroup
from flask_jwt_extended import get_current_user
from app.validators.files import CreateGroupFile,DeleteOrRecoverGroupFile,GetGroupFile,CreateOrUpdateGroupForm,FileType,SetFileTitle
from app.libs.utils import get_page_from_query, json_res, paginate
from lin.db import get_total_nums
from flask import current_app
import re,os
from lin.core import File
from app.extensions.file.config import FILE
_store_dir = FILE['STORE_DIR']
file_group_api = Redprint('file_group')
from datetime import datetime
FileMap= {"img":ImgGroup,'txt':TxtGroup,'audio':AudioGroup,'video':VideoGroup}
# 文件查看
@file_group_api.route('/file', methods=['GET'])
@login_required
def get_all_file():
    # 1 img ,2 txt,3 audio,4 video
    form = GetGroupFile().validate_for_api()
    folder_id = int(form.folder_id.data)
    isDelete = int(form.isDelete.data)
    current_path = current_app.static_url_path
    site_domain = current_app.config.get('SITE_DOMAIN') \
        if current_app.config.get('SITE_DOMAIN') else 'http://127.0.0.1:2100'
    join_path = site_domain + current_path
    start, count = paginate()
    FileManage=FileMap[form.type.data]
    if(isDelete):
        paths = FileManage.query.filter(
            db.and_(
                FileManage.folder_id == folder_id,
                FileManage.delete_time != None
            ) if folder_id else FileManage.delete_time != None
        ).order_by(db.desc('create_time')).offset(
            start).limit(count).all()
    else:
        paths = FileManage.query.filter(
            db.and_(
                FileManage.folder_id == folder_id,
                FileManage.delete_time == None
            ) if folder_id else FileManage.delete_time == None
        ).order_by(db.desc('create_time')).offset(
            start).limit(count).all()
    for x in paths:
        x.path=x.path if re.search(r'http',x.path) else join_path+x.path
    total = get_total_nums(FileManage)
    total_page = math.ceil(total / count)
    page = get_page_from_query()
    return json_res(count=count, items=paths, page=page, total=total, total_page=total_page)
# 文件恢复
@file_group_api.route('/recover/file', methods=['PUT'])
@route_meta(auth='恢复文件', module='文件管理')
@group_required
def recover_group_file():
    form = DeleteOrRecoverGroupFile().validate_for_api()
    # 1 img ,2 txt,3 audio,4 video
    FileManage=FileMap[form.type.data]
    with db.auto_commit():
        FileManage.query.filter(
            FileManage.id.in_(form.ids.data),
        ).update({FileManage.delete_time: None}, synchronize_session=False)
    return Success(msg='文件已恢复')
# 文件新增
@file_group_api.route('/file', methods=['POST'])
@route_meta(auth='新增文件', module='文件管理')
@group_required
def create_group_file():
    form = CreateGroupFile().validate_for_api()
    print(form.type.data,'form.type.data')
    FileManage = FileMap[form.type.data]
    # 1 img ,2 txt,3 audio,4 video
    current_path = current_app.static_url_path
    site_domain = current_app.config.get('SITE_DOMAIN') \
        if current_app.config.get('SITE_DOMAIN') else 'http://127.0.0.1:2100'
    replace_path = site_domain+current_path
    current_user=get_current_user()
    with db.auto_commit():
        for item in form.paths.data:
            # real_path=item.path.replace(replace_path,'')
            real_path=item['path'].replace(replace_path,'')
            one = FileManage.query.filter_by(path=real_path,folder_id=form.folder_id.data).first()
            if not one:
                File.query.filter_by(path=real_path).update({File.active:1}, synchronize_session=False)
                FileManage.create(
                    folder_id=form.folder_id.data,
                    path=real_path,
                    title=item['title'],
                    auth_id=current_user.id
                )

    return Success(msg='添加成功')
# 文件删除
@file_group_api.route('/file', methods=['DELETE'])
@route_meta(auth='删除文件', module='文件管理')
@group_required
def delete_group_file():
    form = DeleteOrRecoverGroupFile().validate_for_api()
    isClear=int(form.isClear.data)
    FileManage = FileMap[form.type.data]
    # 1 img ,2 txt,3 audio,4 video,删除文件
    if (isClear):
        fileList=FileManage.query.filter(
                FileManage.id.in_(form.ids.data),
            ).all()
        with db.auto_commit():
            for i in fileList:
                i.hard_delete()
                # file_path=_store_dir+i.path
                # if os.path.exists(file_path):
                #     os.remove(file_path)
    else:
        with db.auto_commit():
            FileManage.query.filter(
                FileManage.id.in_(form.ids.data),
            ).update({FileManage.delete_time: datetime.now()}, synchronize_session=False)
    return Success(msg='回收站已清空' if isClear else '删除成功')
@file_group_api.route('/file', methods=['PUT'])
@login_required
def set_title():
    # 0 img ,1 txt,2 audio,3 video
    form = SetFileTitle().validate_for_api()
    FileManage = FileMap[form.type.data]
    file = FileManage.query.filter_by(id=form.id.data).first()
    if file is None:
        raise NotFound(msg='没有找到相关文件')
    file.update(
        title=form.title.data,
        commit=True
    )
    return Success(msg='修改成功')
@file_group_api.route('', methods=['GET'])
@login_required
def get_all():
    # 0 img ,1 txt,2 audio,3 video
    form = FileType().validate_for_api()
    groups = FileGroup.get_all(form.type.data)
    return jsonify(groups)


@file_group_api.route('', methods=['POST'])
@route_meta(auth='新建文件分组', module='文件分组')
@group_required
def create_group():
    form = CreateOrUpdateGroupForm().validate_for_api()
    FileGroup.new_group(form)
    return Success(msg='新建文件分组成功')


@file_group_api.route('/<bid>', methods=['PUT'])
@route_meta(auth='修改文件分组', module='文件分组')
@group_required
def update_group(bid):
    form = CreateOrUpdateGroupForm().validate_for_api()
    FileGroup.edit_group(bid, form)
    return Success(msg='更新文件分组成功')


@file_group_api.route('/<bid>', methods=['DELETE'])
@route_meta(auth='删除文件分组', module='文件分组')
@group_required
def delete_group(bid):
    form = FileType().validate_for_api()
    FileManage = FileMap[form.type.data]
    hasFile=FileManage.query.filter_by(folder_id=bid).first()
    if hasFile:
        raise Forbidden(msg='文件夹下(或文件夹下的回收站)有文件不能删除')
    FileGroup.remove_group(bid)
    return Success(msg='删除文件分组成功')
