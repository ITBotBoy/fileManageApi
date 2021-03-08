"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, String, Integer,Text


class ImgGroup(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String(200), nullable=False)
    title = Column(String(100), nullable=False)
    folder_id = Column(Integer, nullable=False)
    auth_id = Column(Integer, nullable=False)
    info = Column(Text)
    like = Column(Integer, default=0)
    collect = Column(Integer, default=0)
    download = Column(Integer, default=0)

