from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)

db_name = 'exercises.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Accessories(db.Model):
    __tablename__ = "accessories"
    id = db.Column(db.Integer, primary_key=True)
    muscle = db.Column(db.String)
    name = db.Column(db.String)

@app.route('/')
def default():
    return redirect(url_for("home"))

@app.route('/home')
def home():
        return render_template("main.html")

@app.route('/<muscle>')
def flex(muscle):
    try:
        accessories = Accessories.query.filter_by(muscle = muscle).order_by(desc(Accessories.name)).all()
        accessory_text = '<ul>'
        for accessory in accessories:
            accessory_text += '<li>' + accessory.name + ", " + accessory.muscle + '</li>'
        accessory_text += '</ul>'
        return accessory_text
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

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

@app.route('/new')
def new():
    return render_template("questionnaire.html")

if (__name__ == "__main__"):
    app.run(debug=True)