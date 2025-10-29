from app import app, db
from models import Quiz, Question
import json
from slugify import slugify

with app.app_context():
    if Quiz.query.filter_by(slug='sample-quiz').first():
        print('Sample already exists.')
    else:
        q = Quiz(title='Sample Quiz', slug='sample-quiz', description='Seeded quiz')
        db.session.add(q); db.session.commit()
        for i in range(1, 6):
            choices = ['A','B','C','D']
            correct = i%4
            qq = Question(quiz_id=q.id, text=f'Question {i}', choices_json=json.dumps(choices), correct=correct)
            db.session.add(qq)
        db.session.commit()
        print('Seeded sample quiz.')
