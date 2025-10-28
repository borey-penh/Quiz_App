from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ----------------- Quiz Questions -----------------
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Boolean, nullable=False)
    explanation = db.Column(db.Text, nullable=True)

# ----------------- Participants / Leaderboard -----------------
class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f'<Score {self.name} {self.score}>'

