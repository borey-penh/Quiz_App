from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class QuizMetaForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Description')
    submit = SubmitField('Create quiz')

class QuestionForm(FlaskForm):
    text = TextAreaField('Question text', validators=[DataRequired(), Length(min=1)])
    choice0 = StringField('Choice 1', validators=[DataRequired()])
    choice1 = StringField('Choice 2', validators=[DataRequired()])
    choice2 = StringField('Choice 3 (optional)')
    choice3 = StringField('Choice 4 (optional)')
    correct = IntegerField('Correct choice index (0..3)', validators=[DataRequired(), NumberRange(min=0, max=3)])
    submit = SubmitField('Add question')
