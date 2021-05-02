from . import db







class Question(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    details = db.Column(db.Text(), nullable = False)
    answer = db.Column(db.String(64), nullable=False)
    incorrect = db.Column(db.Integer())
    correct = db.Column(db.Integer())
    category = db.Column(db.String(64), nullable = False)


class User(db.Model):

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    country = db.Column(db.String(64))
    score = db.Column(db.Integer())



# the idea is to use the category class to differenciate the question. so will pick a random choice from that category to display

# i can create then a route question/category to display all question in differents parts

# categoryes
# mathkids
# math advanced
# math teenager
# math 