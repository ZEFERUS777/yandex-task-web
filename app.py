from flask import Flask, request, redirect, render_template, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from blueprint.rest_api import jobs_bp, api_bp
from data.models import User, Jobs, db, Api_Keys, TeamLead
from secrets import token_urlsafe
from data.wtf_forms import LoginForm, RegisterForm, JobForm, Reg_Api_key, Add_Team_Lead

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "mandale"

log_m = LoginManager()
log_m.init_app(app)
log_m.login_view = "login"

app.register_blueprint(jobs_bp)
app.register_blueprint(api_bp)
db.init_app(app)


@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html")


@log_m.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


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
            tm_id = forma.Team_lead_id.data
            tm_email = TeamLead.query.filter_by(team_lead_id=tm_id).first()
            job = Jobs(
                job_title=forma.Job_Title.data,
                team_lead_id=tm_id,
                work_size=forma.Work_Size.data,
                collaborators=forma.Collaborators.data,
                finish=forma.finish.data
            )
            db.session.add(job)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            print(e)
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
@login_required
def create_api_key():
    form = Reg_Api_key()
    if request.method == "POST":
        try:
            key = token_urlsafe(16)
            email = current_user.email
            aap = Api_Keys.query.filter_by(email_address=email).first()
            if aap:
                return render_template("reg_api.html", form=form, error="Вы уже создавали ключ")
            key_f = Api_Keys(email_address=email)
            key_f.set_password(key)
            db.session.add(key_f)
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            user.api_k = key
            db.session.add(user)
            db.session.commit()
            return render_template("vision_api.html", api_key=key)
        except Exception as e:
            print(e)
            return render_template("reg_api.html", form=form,
                                   error="Ошибка при работе с базой данных")
    return render_template("reg_api.html", form=form)


@app.route("/jobs_vision")
@login_required
def jobs_vision():
    jobs = Jobs.query.all()
    return render_template("jobs_list.html", jobs=jobs, title="Список работ")


@app.route("/profile")
@login_required
def profile():
    if current_user.api_k is None:
        return render_template("profile.html", user_name=current_user.email, api_key="Не зарегистрирован")
    return render_template("profile.html", user_name=current_user.email, api_key=current_user.api_k)


@app.route("/add_lead", methods=["GET", "POST"])
@login_required
def add_lead():
    form = Add_Team_Lead()
    if request.method == "POST":
        name = form.lead_name.data
        lead_id = form.lead_id.data
        email = form.email_lead.data
        if TeamLead.query.filter_by(email=email).first() is not None or TeamLead.query.filter_by(team_lead_id=lead_id).first() is not None:
            return render_template("team_leads_add.html", form=form, error="Лидер уже существует")
        lead = TeamLead(name=name, team_lead_id=lead_id, email=email)
        db.session.add(lead)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("team_leads_add.html", form=form)


@app.route("/team_leads")
@login_required
def team_leads():
    leads = TeamLead.query.all()
    return render_template("leads.html", leads=leads)


if __name__ == '__main__':
    app.run()
