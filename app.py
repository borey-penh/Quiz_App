from flask import Flask, render_template, request, redirect, url_for
from models import db, Question, Participant
from data_seed import seed_data
from sqlalchemy import func
from flask import render_template
from models import Question


app = Flask(__name__)
app.secret_key = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret_key'

db.init_app(app)

with app.app_context():
    db.create_all()
    if Question.query.count() == 0:
        seed_data(db, Question)



@app.route('/')
def index():
    categories = db.session.query(db.func.lower(db.func.trim(Question.category))).distinct().all()
    categories = [c[0].capitalize() for c in categories]
    return render_template('index.html', categories=categories)

@app.route('/quiz/<category>', methods=['GET', 'POST'])
def quiz(category):
    index = int(request.args.get('index', 0))
    score = int(request.args.get('score', 0))
    # questions = Question.query.filter_by(category=category).all()
    questions = Question.query.filter(Question.category.ilike(category)).all()
    total = len(questions)

    if total == 0:
        return f"No questions in category {category}."
    if index >= total:
            return redirect(url_for('finish', score=score))

    question = questions[index]


    if request.method == 'POST':
        answer = request.form.get('answer')
        if (answer == 'true' and question.answer) or (answer == 'false' and not question.answer):
            score += 1
        # next_index = index + 1
        
        return redirect(url_for('quiz', category=category, index=index+1, score=score))

    return render_template('quiz.html',
                           question=question,
                           index=index,
                           total=total,
                           score=score,
                           category=category)

@app.route('/finish', methods=['GET', 'POST'])
def finish():
    score = int(request.args.get('score', 0))
    if request.method == 'POST':
        name = request.form.get('name')
        participant = Participant(name=name, score=score)
        db.session.add(participant)
        db.session.commit()
        return redirect(url_for('leaderboard'))

    top = Participant.query.order_by(Participant.score.desc()).limit(10).all()
    return render_template('quiz.html', final_score=score, top=top)

@app.route('/leaderboard')
def leaderboard():
    top = Participant.query.order_by(Participant.score.desc()).limit(10).all()
    return render_template('leaderboard.html', top=top)




if __name__ == '__main__':
    app.run(debug=True)
