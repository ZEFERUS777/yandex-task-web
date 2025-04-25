from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, validators, IntegerField
from flask_wtf import FlaskForm



class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[validators.DataRequired()])
    password = PasswordField('Пароль', validators=[
                             validators.DataRequired(), validators.length(min=8, max=15)])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")


class JobForm(FlaskForm):
    Job_Title = StringField(
        "Название работы",
        validators=[validators.DataRequired()],
        render_kw={"class": "form-control"},
    )

    Team_lead_id = IntegerField(
        "ID капитана",
        validators=[validators.DataRequired()],
        render_kw={"class": "form-control"}
    )

    Work_Size = IntegerField(
        "Размер работы",
        validators=[validators.DataRequired()],
        render_kw={"class": "form-control"}
    )

    Collaborators = StringField(
        "Коллеги",
        validators=[validators.DataRequired()],
        render_kw={"class": "form-control"}
    )

    finish = BooleanField(
        "Окончено",
        render_kw={"class": "form-check-input"}
    )

    sub = SubmitField(
        "Отправить",
        render_kw={"class": "btn btn-primary"}
    )


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[
                             validators.DataRequired()])
    submit = SubmitField('Register')


class Reg_Api_key(FlaskForm):
    sub_btn = SubmitField("Подтвердить")
