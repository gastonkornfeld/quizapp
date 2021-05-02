  
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo



class AddQuestionForm(FlaskForm):
    details = StringField('Question details',
                        validators=[DataRequired(), Length(max=10000)]) 
    answer = StringField('Correct answer',
                        validators=[DataRequired(), Length(max=10000)])                   
    correct = StringField('Points for correct answer',
                        validators=[DataRequired(), Length(max=10)])
    wrong = StringField('Points for wrong answer',
                        validators=[DataRequired(), Length(max=10)])
    category = StringField('Category',
                        validators=[DataRequired(), Length(max=10)])
    submit = SubmitField('Add question')

class AnswerForm(FlaskForm):
    answer = StringField('Write your answer here:',
                        validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Check Answer')

class CategoryForm(FlaskForm):
    category = StringField('Which category you want to look for:',
                        validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Search category')


class AddUserForm(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    country = StringField('Country',
                        validators=[DataRequired()])
    submit = SubmitField('ADD USER')

class LoginForm(FlaskForm):
    name = StringField('Name',
                        validators=[DataRequired(), Length(min=2, max=20)])
    country = StringField('Country',
                        validators=[DataRequired()])
    submit = SubmitField('Login')

