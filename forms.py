from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class LeaderboardForm(FlaskForm):
    name = StringField('Name', validators=[Length(max=120)])
    submit = SubmitField('Save to Leaderboard')
