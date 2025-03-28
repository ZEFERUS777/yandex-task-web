from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, validators, IntegerField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mandale'

db = SQLAlchemy(app)
log_m = LoginManager()
log_m.init_app(app)
log_m.login_view = 'login'




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
        # Удален validators.DataRequired()
        render_kw={"class": "form-check-input"}
    )

    sub = SubmitField(
        "Submit",
        render_kw={"class": "btn btn-primary"}  # Классы для кнопки
    )


class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    submit = SubmitField('Register')


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password_bash = db.Column(db.String(120))
    
    
    def set_password(self, password):
        self.password_bash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_bash, password)


class Jobs(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    Job_Title = db.Column(db.String(80), nullable=False)
    Team_lead_id = db.Column(db.Integer, nullable=False)
    Work_Size = db.Column(db.Integer, nullable=False)
    Collaborators = db.Column(db.String(80), nullable=False)
    finish = db.Column(db.Boolean, nullable=False)


@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html")


# Добавьте этот код после создания экземпляра LoginManager и определения класса User

@log_m.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    return render_template("login.html", title='Авторизация', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))  # Используйте url_for


@app.route("/addjob", methods=['GET', 'POST'])
@login_required
def addjob():
    forma = JobForm()
    if forma.validate_on_submit():  # Используйте validate_on_submit для формы
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
            return redirect(url_for('index'))  # Используйте url_for
        except Exception as e:
            return redirect(url_for('addjob'))
    return render_template("job.html", title='Добавить работу', form=forma)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        try:
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                return render_template("register.html", form=form, error="Пользователь уже существует")
            new_user = User(email=form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        except Exception as e:
            return render_template("register.html", form=form, error=True)
    return render_template("register.html", form=form)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
