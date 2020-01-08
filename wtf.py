from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, BooleanField, SelectField, RadioField, TextField
from wtforms.validators import DataRequired, EqualTo


class userInformation(FlaskForm):
    account = StringField('账号', validators=[DataRequired()])
    password = PasswordField('旧密码', validators=[DataRequired()])
    password1 = PasswordField('新密码', validators=[DataRequired(), EqualTo(password, '密码填入不一致')])
    contact = StringField('联系方式', validators=[DataRequired()])
    sex = RadioField('性别', choices=[('0', '男'), ('1', '女')], validators=[DataRequired()])
    departmentSelect = SelectField('部门：', choices=[
        ('one', '人力资源部'),
        ('two', '企划部'),
        ('three', '市场部'),
        ('four', '财务部')
    ])
    inPut = SubmitField('提交')


class appendMeeting(FlaskForm):
    mrID = StringField('mrID', validators=[DataRequired()])
    mrName = StringField('mrName', validators=[DataRequired()])
    mrCapacity = StringField('mrCapacity', validators=[DataRequired()])
    mrContent = StringField('mrContent', validators=[DataRequired()])
    submit = SubmitField('立即添加')


class reservationMeeting(FlaskForm):
    mID = StringField('mID', validators=[DataRequired()])
    mName = StringField('mName', validators=[DataRequired()])
    resPerson = StringField('resPerson', validators=[DataRequired()])
    mrName = StringField('mrName', validators=[DataRequired()])
    startTime = DateField('startTime', format='%Y-%m-%d')
    endTime = DateField('endTime', format='%Y-%m-%d')
    mContent = StringField('mContent', validators=[DataRequired()])
    submit = SubmitField('立即添加')


class updataMR(FlaskForm):
    mrID = StringField('mID', validators=[DataRequired()])
    mrName = StringField('mrName', validators=[DataRequired()])
    mrCapacity = StringField('mrCapacity', validators=[DataRequired()])
    mrContent = StringField('mrContent', validators=[DataRequired()])
    submit = SubmitField('立即修改')
