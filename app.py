from flask import Flask, request, redirect, render_template, url_for
from flask_wtf import FlaskForm
from flask_login import LoginManager, login_user, logout_user, login_required
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, validators, IntegerField
from werkzeug.security import generate_password_hash, check_password_hash
from blueprint.rest_api import jobs_bp
from data.models import User, Jobs, db, Api_Keys
from secrets import token_urlsafe


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "mandale"

log_m = LoginManager()
log_m.init_app(app)
log_m.login_view = "login"

app.register_blueprint(jobs_bp)

db.init_app(app)


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
    email = EmailField("Введите свою почту", validators=[
                       validators.DataRequired()])
    sub_btn = SubmitField("Подтвердить")


@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html")


@log_m.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template("login.html", title='Авторизация', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/addjob", methods=['GET', 'POST'])
@login_required
def addjob():
    forma = JobForm()
    if forma.validate_on_submit():
        try:
            job = Jobs(
                Job_Title=forma.Job_Title.data,
                Team_lead_id=forma.Team_lead_id.data,
                Work_Size=forma.Work_Size.data,
                Collaborators=forma.Collaborators.data,
                finish=forma.finish.data
            )
            db.session.add(job)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return redirect(url_for('addjob'))
    return render_template("job.html", title='Добавить работу', form=forma)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        return render_template("register.html", form=form, error="Пользователь уже существует")
    if request.method == 'POST':
        try:

            new_user = User(email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        except Exception as e:
            return render_template("register.html", form=form, error="Ошибка регистрации, попробуйте снова")
    return render_template("register.html", form=form)


@app.route("/create_api_key", methods=["GET", "POST"])
def create_api_key():
    form = Reg_Api_key()
    if request.method == "POST":
        try:
            key = token_urlsafe(16)
            email = form.email.data
            aap = Api_Keys.query.filter_by(email_address=email).first()
            if aap:
                return render_template("reg_api.html", form=form, error="Вы уже создавали ключ")
            key_f = Api_Keys(email_address=email)
            key_f.set_password(key)
            db.session.add(key_f)
            db.session.commit()
            return render_template("vision_api.html", api_key=key)
        except Exception:
            return render_template("reg_api.html", form=form, 
                                   error="Ошибка при работе с базой данных")
    return render_template("reg_api.html", form=form)


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
