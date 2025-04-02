from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    password_bash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_bash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_bash, password)


class Jobs(db.Model, SerializerMixin):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    Job_Title = db.Column(db.String(80), nullable=False)
    Team_lead_id = db.Column(db.Integer, nullable=False)
    Work_Size = db.Column(db.Integer, nullable=False)
    Collaborators = db.Column(db.String(80), nullable=False)
    finish = db.Column(db.Boolean, nullable=False)

    def __init__(self, job_title: str, team_lead_id: int, work_size: int, collaborators: str, finish: bool = False):
        self.Job_Title = job_title
        self.Team_lead_id = team_lead_id
        self.Work_Size = work_size
        self.Collaborators = collaborators
        self.finish = finish


class Api_Keys(db.Model):
    __tablename__ = "api_keys"
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(80), nullable=False)
    key = db.Column(db.String(80), nullable=False)

    def set_password(self, password):
        self.key = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.key, password)
