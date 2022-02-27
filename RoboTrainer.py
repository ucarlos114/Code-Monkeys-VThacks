from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from sqlalchemy.sql.expression import func, select

app = Flask(__name__)

########################### DATABASE SETUP ############################
db_name = 'exercises.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Accessories(db.Model):
    __tablename__ = "accessories"
    id = db.Column(db.Integer, primary_key=True)
    muscle = db.Column(db.String)
    name = db.Column(db.String)
########################### DATABASE SETUP ############################


"""     Both lead to default home page      """
@app.route('/')
def default():
    return redirect(url_for("home"))

@app.route('/home')
def home():
        return render_template("main.html")


"""     Show all exercises in database      """
@app.route('/allexercises')
def all():
    chests = Accessories.query.filter_by(muscle = "chest").order_by(Accessories.id).all()
    shoulders = Accessories.query.filter_by(muscle = "shoulders").order_by(Accessories.id).all()
    triceps = Accessories.query.filter_by(muscle = "triceps").order_by(Accessories.id).all()
    backs = Accessories.query.filter_by(muscle = "back").order_by(Accessories.id).all()
    biceps = Accessories.query.filter_by(muscle = "biceps").order_by(Accessories.id).all()
    legs = Accessories.query.filter_by(muscle = "legs").order_by(Accessories.id).all()

    return render_template("exercises.html", chests=chests, shoulders=shoulders, triceps=triceps,
            backs=backs, biceps=biceps, legs=legs)


"""     Questionnaire required to create a new program      """
@app.route('/new', methods=["POST","GET"])
def new():
    if request.method == "POST":
        name = request.form['name']
        days = request.form['days']
        exp = request.form['exp']
        return redirect(url_for("process", name=name, days=days, exp=exp))
    else:
        return render_template("questionnaire.html")


"""     Process the info from questionnaire     """
@app.route("/process<name><days>days<exp>exp")
def process(name, days, exp):    
    if name == '':
          name = 'User'
    return f"<h1>Name: {name}\n Days: {days}\n Experience: {exp}"

"""     Run app     """
if (__name__ == "__main__"):
    app.run(debug=True)