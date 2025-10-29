from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, pw):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(pw)
    def check_password(self, pw):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, pw)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    submissions = db.relationship('Submission', backref='quiz', lazy=True)
    questions = db.relationship('Question', backref='quiz', cascade='all, delete-orphan')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    text = db.Column(db.Text, nullable=False)
    choices_json = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Integer, nullable=False)
    def choices(self):
        return json.loads(self.choices_json)

class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120))
    user_email = db.Column(db.String(200))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    answers_json = db.Column(db.Text)
    score = db.Column(db.Integer)
    score = db.Column(db.Float)
    answers = db.Column(db.PickleType)
    def answers(self):
        return json.loads(self.answers_json)
