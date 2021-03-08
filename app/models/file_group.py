"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from lin.exception import NotFound, ParameterException
from sqlalchemy import Column, String, Integer
from lin.interface import BaseCrud as Base
from flask_jwt_extended import get_current_user
class FileGroup(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent_id = Column(Integer, nullable=False,default=0)
    operate_id = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(500))
    @classmethod
    def get_all(cls,type):
        if type is not None:
            groups = cls.query.filter(FileGroup.type == type).all()
        else:
            groups = cls.query.all()
        return groups


    @classmethod
    def new_group(cls, form):
        group = FileGroup.query.filter_by(parent_id=form.parent_id.data, name=form.name.data, type=form.type.data).first()
        if group is not None:
            raise ParameterException(msg='分组已存在')
        current_user=get_current_user()
        FileGroup.create(
            parent_id=form.parent_id.data,
            operate_id=current_user.id,
            type=form.type.data,
            name=form.name.data,
            description=form.description.data,
            commit=True
        )
        return True

    @classmethod
    def edit_group(cls, bid, form):
        group = FileGroup.query.filter_by(id=bid).first()
        if group is None:
            raise NotFound(msg='没有找到相关分组')

        group.update(
            id=bid,
            parent_id=form.parent_id.data,
            name=form.name.data,
            description=form.description.data,
            commit=True
        )
        return True

    @classmethod
    def remove_group(cls, bid):
        # 分组下有内容不可删除
        group = cls.query.filter_by(id=bid).first()
        if group is None:
            raise NotFound(msg='没有找到相关分组')
        group.delete(commit=True)
        return True
