from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, csrf, CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from wtforms import StringField, SubmitField, PasswordField, EmailField, BooleanField, validators, IntegerField
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms.widgets import Input



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///flask.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mandale'                                                                                       

db = SQLAlchemy(app)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[validators.DataRequired()])
    password = PasswordField('Пароль', validators=[validators.DataRequired(), validators.length(min=8, max=15)])
    remember_me = BooleanField("Запомнить меня")
    submit = SubmitField("Войти")
    
  # Импорт с большой буквы!

class JobForm(FlaskForm):
    Job_Title = StringField(
        "Название работы",
        validators=[validators.DataRequired()],
        render_kw={"class": "form-control"},  # Более простой способ
        widget=Input()  # Если нужен кастомный виджет
    )
    
    Team_lead_id = StringField(
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
        validators=[validators.DataRequired()],
        render_kw={"class": "form-check-input"}  # Специальный класс для чекбоксов
    )
    
    sub = SubmitField(
        "Submit",
        render_kw={"class": "btn btn-primary"}  # Классы для кнопки
    )

    
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


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
    return render_template("login.html", title='Авторизация', form=form)



@app.route("/addjob", methods=['GET', 'POST'])
def addjob():
    forma = JobForm()
    if request.method == "POST":
        job = Jobs(Job_Title=forma.Job_Title.data, Team_lead_id=forma.Team_lead_id.data, 
                   Work_Size=forma.Work_Size.data, Collaborators=forma.Collaborators.data, 
                   finish=forma.finish.data)
        return redirect("/")
    return render_template("job.html", title='Добавить работу', form=forma)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)