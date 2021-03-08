from lin import manager
from wtforms import DateTimeField, PasswordField, FieldList, IntegerField,FormField, StringField,RadioField
from wtforms.validators import DataRequired, Regexp, EqualTo, length, Optional, NumberRange


from lin.forms import Form
class FileType(Form):
    type = RadioField('文件类型', choices=[('img','img'),('txt','txt'),('video','video'),('audio','audio')])
class SetFileTitle(FileType):
    id = IntegerField('id',
                             validators=[DataRequired(message='请输入id字段')])
    title = StringField('分组id',
                             validators=[DataRequired(message='请输入title字段'),length(min=2, max=50, message='title长度必须在2~50之间')], default=0)
class CreateOrUpdateGroupForm(FileType):
    parent_id = IntegerField('分组id',
                            validators=[Optional()],default=0)
    name = StringField(validators=[DataRequired(message='请输入name字段'),length(min=2, max=50, message='name长度必须在2~50之间')])
    description = StringField(validators=[Optional(),length(min=3, max=500, message='description长度必须在3~500之间')])
class CreateGroupFile(FileType):
    folder_id = IntegerField('分组id',
                             validators=[DataRequired(message='请输入folder_id字段')])
    paths = FieldList(StringField(validators=[DataRequired(message='请输入paths字段')]))

class DeleteOrRecoverGroupFile(FileType):
    ids = FieldList(IntegerField(validators=[DataRequired(message='请输入ids字段')]))
    isClear = IntegerField('清空回收站',
                             validators=[Optional()], default=0)

class GetGroupFile(FileType):
    folder_id = IntegerField('分组id',
                             validators=[Optional()], default=0)
    isDelete = IntegerField('查看回收站',
                           validators=[Optional()], default=0)