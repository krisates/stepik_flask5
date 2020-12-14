from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()


class OrderForm(FlaskForm):
   # name = StringField('Ваше имя', [InputRequired(message="Необходимо указать имя")])
    address = StringField('Адрес')
    email = StringField('Email', [Email(message="Необходимо указать email")])
    phone = StringField('Телефон', [InputRequired(message="Необходимо указать телефон")])
    price = HiddenField('price')
    dishes = HiddenField('dishes')
    submit = SubmitField()


class AuthForm(FlaskForm):
    email = StringField('Email', [Email(message="Необходимо указать email")])
    password = PasswordField('Password', [InputRequired(message="Необходимо указать имя"), Length(5)])
    submit = SubmitField()