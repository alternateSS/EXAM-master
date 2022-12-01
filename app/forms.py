from flask_wtf import FlaskForm
import wtforms as ws
from wtforms import ValidationError
from flask_login import current_user
from app import app
from .models import Employee, User
from flask import flash


class EmployeeForm(FlaskForm):
    fullname = ws.StringField('ФИО Кандидата', validators=[ws.validators.DataRequired(), ])
    phone = ws.StringField('Номер телефона', validators=[ws.validators.DataRequired(), ])
    short_info = ws.TextAreaField('Краткая информация', validators=[ws.validators.DataRequired(), ])
    experience = ws.IntegerField('Опыт работы в годах', validators=[ws.validators.DataRequired(), ])
    preferred_position = ws.StringField('Предпочитаемая позиция', default=None)
    user_id = ws.SelectField('Менеджер', choices=[])
    submit = ws.SubmitField('Сохранить')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_choices = []
        with app.app_context():
            for user in User.query.all():
                self.user_choices.append((user.id, user.username))
            self._fields['user_id'].choices = self.user_choices

    def validate_fullname(self, field):
        names_split = field.data.split(' ')
        if len(names_split) == 1:
            raise ValidationError(flash('ФИО не может состоять из одного слова', 'danger'))
        for name in names_split:
            if not name.isalpha():
                raise ValidationError(flash('В ФИО не должно быть спец символов и чисел', 'danger'))


class UserForm(FlaskForm):
    username = ws.StringField('Имя пользователя', validators=[
        ws.validators.DataRequired(), ])
    password = ws.PasswordField('Пароль', validators=[
        ws.validators.DataRequired(),
        ws.validators.Length(min=8, max=22)
    ])
    submit = ws.SubmitField('Сохранить')