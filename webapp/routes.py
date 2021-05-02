import flask
import random
import flask_login
from . import app, funct
from . import models
from . import db
from . import forms

login_manager = flask_login.LoginManager()

@app.route('/')
def init():
    flask.session['user__name'] = 'logout'
    return flask.render_template('index.html')


@app.route("/index", methods = ['GET', 'POST'])
def index():
    
            
  
    # if the user is logged retrieve it to the template if not a general template
    if flask.session['user__name'] != 'logout':
        active_user = flask.session['user__name']
        score = flask.session['user__score']
        form = forms.CategoryForm()
        if flask.request.method == 'POST':
            category = form.category.data
            return flask.redirect(flask.url_for('category', category = category))
        else:
            return flask.render_template('index.html', user = active_user, score = score, form = form) 
    else:
        return flask.render_template('index.html')

@app.route("/all")
def all():
    all_questions = models.Question.query.all() #order by id
    # all_questions = models.Question.query.order_by(models.Question.category) # by category
    return flask.render_template('all.html', questions = all_questions)



@app.route("/add_question", methods = ['GET', "POST"])
def add():
    form = forms.AddQuestionForm()
    if form.validate_on_submit():
        desc = form.details.data
        answer = form.answer.data
        correct = form.correct.data
        wrong = form.wrong.data
        category = form.category.data
        question = models.Question(details = desc, answer = answer, incorrect = wrong, correct = correct, category = category)
        db.session.add(question)
        db.session.commit()
        flask.flash("Question added to the database", 'success')
        return flask.redirect(flask.url_for('all'))
    return flask.render_template('add_question.html', form = form)



@app.route('/category/<category>', methods = ['GET', "POST"])
def category(category):
    
    form = forms.AnswerForm()
    if flask.request.method == 'POST':
           
        if form.validate_on_submit():
            answer = form.answer.data
            to_chek = models.Question.query.get(flask.session['id_question'])
            answer1 = to_chek.answer
            # here checking the answer if it is correct or not 
            # an then update the score of the user on session and database
            if answer.lower() == answer1.lower():
                flask.flash('Correct', 'success')
                flask.session['user__score'] = int(flask.session['user__score']) + to_chek.correct
                user = models.User.query.filter_by(name = flask.session['user__name']).first()
                user.score = flask.session['user__score']
                db.session.commit()
                return flask.redirect(flask.url_for('category', category = category))
            else:
                flask.flash("Incorrect. The correct answer is " + models.Question.query.get(flask.session['id_question']).answer, 'danger')
                flask.session['user__score'] = int(flask.session['user__score']) + to_chek.incorrect
                user = models.User.query.filter_by(name = flask.session['user__name']).first()
                user.score = flask.session['user__score']
                db.session.commit()
                return flask.redirect(flask.url_for('category', category = category))
    else:
        # if the category they are searching is not empty so i want to take all the questions
        # if it is empty i need to display a message
        if models.Question.query.filter_by(category = category).first() != None:
            all_question_category = models.Question.query.filter_by(category = category)
            random_question = random.choice(list(all_question_category))
            flask.session['id_question'] = random_question.id
            score = flask.session['user__score']
    
            return flask.render_template('category.html', questions = all_question_category, random = random_question, form = form, score = score)
        else:
            return flask.render_template('category_not_found.html', category = category)


@app.route('/users')
def users():
    all_users =  models.User.query.all()
    return flask.render_template('users.html', all_users = all_users)


@app.route('/add_user', methods=['GET', "POST"])
def add_user():
    form = forms.AddUserForm()
    if form.validate_on_submit():
        name = form.name.data
        
        country = form.country.data
        new_user = models.User(name = name,country = country, score = 0)
        db.session.add(new_user)
        db.session.commit()
        flask.flash(f'Username added Succesfully', 'success')

        return flask.redirect(flask.url_for('users'))
    return flask.render_template('add_user.html', title = 'ADD user', form = form)




@app.route('/login', methods=['GET', "POST"])
def login():
    # all_users = models.User.query.all()
    form = forms.LoginForm()
    # add the control of the template if it is already logged
    if flask.session['user__name'] == 'logout':

        if form.validate_on_submit():
            name = form.name.data
            country = form.country.data
            if models.User.query.filter_by(name=name, country = country).first() == None:
                flask.flash(f'The user doesnt exist please sign up', 'danger')
                return flask.redirect(flask.url_for('add_user'))
            else:
                flask.flash(f'Login Succesfully as ' + name, 'success')
                user = models.User.query.filter_by(name=name, country = country).first()
                flask.session['user__name'] = user.name
                flask.session['user__score'] = user.score
                # need to add login session here to keep the track of the user score and save to the database.
                return flask.redirect(flask.url_for('index'))
               
    user = flask.session['user__name']
    return flask.render_template('login.html', form = form, user = user)



@app.route('/logout')
def logout():
    if flask.session['user__name'] != 'logout':
    # when log out want to save the current score of the user to the database, and then empty the session variables
        user = models.User.query.filter_by(name = flask.session['user__name']).first()
        user.score = flask.session['user__score']
        db.session.commit()
        flask.session['user__name'] = 'logout'
        flask.session['user__score'] = 'Not User Logged'
        flask.flash('Log out succesfully', 'success')
        return flask.redirect(flask.url_for('index'))
    else:
        flask.flash('Please Login', 'danger')
        return flask.redirect(flask.url_for('login'))

    # need to add a log out route where is gonna finish the session, also need to make the app only work when
    # logged in. so also display different depending on that.

    # remember to use lowercase to retrieve the answer from the form.





    # Geography categories

@app.route('/geography')
def geography():
   

    if flask.session['user__name'] != 'logout':
        active_user = flask.session['user__name']
        score = flask.session['user__score']
        return flask.render_template('geography.html', user = active_user, score = score) 
    else:
        return flask.render_template('geography.html')


@app.route('/science')
def science():
   

    if flask.session['user__name'] != 'logout':
        active_user = flask.session['user__name']
        score = flask.session['user__score']
        
        return flask.render_template('science.html', user = active_user, score = score) 
    else:
        return flask.render_template('science.html')

@app.route('/logic')
def logic():
   

    if flask.session['user__name'] != 'logout':
        active_user = flask.session['user__name']
        score = flask.session['user__score']
        
        return flask.render_template('logic.html', user = active_user, score = score) 
    else:
        return flask.render_template('logic.html')

@app.route('/math')
def math():
   

    if flask.session['user__name'] != 'logout':
        active_user = flask.session['user__name']
        score = flask.session['user__score']
        
        return flask.render_template('math.html', user = active_user, score = score) 
    else:
        return flask.render_template('math.html')



@app.route('/leaderboard')
def score():
    
    
    all_users = models.User.query.order_by(models.User.score)
    # this logged user is used to retrieve the info in the index template after log in
    logged_user = models.User.query.filter_by(name = flask.session['user__name']).first()


    return flask.render_template('leaderboard.html', users = all_users, logged = logged_user)
