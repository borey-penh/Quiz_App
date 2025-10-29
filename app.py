from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
from slugify import slugify
from flask import Flask, render_template, redirect, url_for, flash
from models import Quiz, Submission  # adjust to your actual models
from flask_login import current_user 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- Models ----------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)
    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    questions = db.relationship('Question', backref='quiz', cascade='all, delete-orphan')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    text = db.Column(db.Text, nullable=False)
    choices_json = db.Column(db.Text, nullable=False)
    correct = db.Column(db.Integer, nullable=False)
    def choices(self):
        return json.loads(self.choices_json)

# ...existing code...
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(120))
    user_email = db.Column(db.String(200))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    quiz = db.relationship('Quiz', backref='submissions')   # <-- add this relationship
    answers_json = db.Column(db.Text)
    score = db.Column(db.Integer)
    def answers(self):
        return json.loads(self.answers_json)
# ...existing code...

# ---------------- Helpers ----------------
def current_user():
    uid = session.get('user_id')
    return User.query.get(uid) if uid else None

def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Please login first.")
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

# ---------------- Routes ----------------
@app.route('/')
def index():
    quizzes = Quiz.query.all()
    return render_template('index.html', quizzes=quizzes, user=current_user())

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pw = request.form['password']
        if User.query.filter_by(email=email).first():
            flash("Email already registered")
            return redirect(url_for('register'))
        u = User(name=name, email=email)
        u.set_password(pw)
        db.session.add(u)
        db.session.commit()
        session['user_id'] = u.id
        flash("Registered successfully")
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        pw = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(pw):
            session['user_id'] = user.id
            flash("Logged in successfully")
            return redirect(url_for('index'))
        flash("Invalid email or password")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out")
    return redirect(url_for('index'))

@app.route('/create_quiz', methods=['GET','POST'])
@login_required
def create_quiz():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        slug_base = slugify(title)
        slug = slug_base
        i = 1
        while Quiz.query.filter_by(slug=slug).first():
            slug = f"{slug_base}-{i}"; i+=1
        q = Quiz(title=title, description=desc, creator_id=current_user().id, slug=slug)
        db.session.add(q); db.session.commit()
        flash("Quiz created")
        return redirect(url_for('edit_quiz', quiz_id=q.id))
    return render_template('create_quiz.html')

@app.route('/quiz/<int:quiz_id>/edit', methods=['GET','POST'])
@login_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if quiz.creator_id != current_user().id:
        flash("Not authorized")
        return redirect(url_for('index'))
    if request.method == 'POST':
        text = request.form['text']
        choices = [request.form['choice0'], request.form['choice1'], request.form.get('choice2',''), request.form.get('choice3','')]
        choices = [c for c in choices if c.strip()!='']
        correct = int(request.form['correct'])
        q = Question(quiz_id=quiz.id, text=text, choices_json=json.dumps(choices), correct=correct)
        db.session.add(q)
        db.session.commit()
        flash("Question added")
        return redirect(url_for('edit_quiz', quiz_id=quiz.id))
    return render_template('edit_quiz.html', quiz=quiz)

@app.route('/take/<slug>', methods=['GET','POST'])
def take_quiz(slug):
    quiz = Quiz.query.filter_by(slug=slug).first_or_404()

    # Prepare questions with indexed choices for template
    questions_indexed = []
    for q_index, q in enumerate(quiz.questions):
        # q.choices() helper exists on Question model in your file
        try:
            choices = q.choices()
        except Exception:
            choices = json.loads(q.choices_json)
        # make choices a list of (choice_index, choice_text) for template robustness
        choices_indexed = list(enumerate(choices))
        questions_indexed.append((q_index, q, choices_indexed))

    if request.method == 'POST':
        # collect answers and compute score
        answers = {}
        score = 0
        for q_index, q, choices in questions_indexed:
            field = f"q-{q_index}"
            val = request.form.get(field)
            if val is None:
                continue
            try:
                selected = int(val)
            except ValueError:
                continue
            answers[q_index] = selected
            if selected == q.correct:
                score += 1

        # determine user info (logged in user or guest fields)
        user = current_user()
        if user:
            user_name = user.name
            user_email = user.email
        else:
            user_name = request.form.get('guest_name', 'Guest')
            user_email = request.form.get('guest_email', '')

        # create submission record
        submission = Submission(
            user_name=user_name,
            user_email=user_email,
            quiz_id=quiz.id,
            answers_json=json.dumps(answers),
            score=score
        )
        db.session.add(submission)
        db.session.commit()

        # redirect to results page
        return redirect(url_for('results', submission_id=submission.id))

    return render_template('quiz_take.html', quiz=quiz, questions=questions_indexed, user=current_user())
# ...existing code...


# ...existing code...
@app.route('/results/<int:submission_id>')
def results(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    quiz = submission.quiz
    questions = quiz.questions
    # parsed answers from JSON (keys will be strings)
    answers = submission.answers()
    return render_template('results.html', submission=submission, quiz=quiz, questions=questions, answers=answers)
# ...existing code...

@app.route('/submit_story', methods=['GET', 'POST'])
@login_required  # make sure user is logged in
def submit_story():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        user = current_user()

        new_story = Story(title=title, content=content, user_id=user.id)
        db.session.add(new_story)
        db.session.commit()

        flash("Story submitted successfully!")
        return redirect(url_for('my_stories'))

    return render_template('submit_story.html', user=current_user())
@app.route('/my_stories')
@login_required
def my_stories():
    user = current_user()
    stories = Story.query.filter_by(user_id=user.id).all()
    return render_template('my_stories.html', stories=stories, user=user)

# ...existing code...
@app.route('/quiz/<int:quiz_id>/participants')
def quiz_participants(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    # group by user email/name to list unique participants with attempt count and best score
    participants = (
        db.session.query(
            Submission.user_name.label('user_name'),
            Submission.user_email.label('user_email'),
            db.func.count(Submission.id).label('attempts'),
            db.func.max(Submission.score).label('best_score')
        )
        .filter(Submission.quiz_id == quiz.id)
        .group_by(Submission.user_email, Submission.user_name)
        .all()
    )
    return render_template('quiz_participants.html', quiz=quiz, participants=participants, user=current_user())
# ...existing code...

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize DB tables
    app.run(debug=True)
