from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, BooleanField, FieldList, SubmitField
from wtforms.validators import DataRequired


class AliasSearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

class ProxySearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    attribute = RadioField('attribute', choices=[('uid', 'Логин'), ('cn', 'ФИО')], default='uid')

class ProxyUnlimForm(FlaskForm):
    limit = StringField('limit')
    noblock = BooleanField('noblock')
    submit = SubmitField('Сохранить')
    cancel = SubmitField('Отмена')

class AliasEditor(FlaskForm):
    description = FieldList(StringField('desc_line'))
    values = FieldList(StringField('value'))
    submit = SubmitField('Сохранить')
    cancel = SubmitField('Отмена')

class AliasCreator(FlaskForm):
    key = StringField('alias_key')
    submit = SubmitField('Создать')
    cancel = SubmitField('Отмена')