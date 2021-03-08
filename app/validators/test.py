from werkzeug.datastructures import ImmutableMultiDict
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange,DataRequired,Regexp,Optional


class Test(Form):  # 接收的是ImmutableMultiDict类型
    group_id = IntegerField('分组id',
                            validators=[DataRequired(message='请输入分组id'), NumberRange(message='分组id必须大于0', min=1)])
    email = StringField('电子邮件', validators=[
        Regexp(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$', message='电子邮箱不符合规范，请输入正确的邮箱'),
        Optional()
    ])


# s = ImmutableMultiDict({'p': 'qwe', 'oe': 13})
# form1 = test(s)
# print(form1.validate())  # True
