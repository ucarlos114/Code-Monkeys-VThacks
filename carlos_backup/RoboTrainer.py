from flask import Flask, render_template
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
def index():
    try:
        accessories = Accessories.query.filter_by(muscle = 'legs').order_by(desc(Accessories.name)).all()
        accessory_text = '<ul>'
        for accessory in accessories:
            accessory_text += '<li>' + accessory.name + ", " + accessory.muscle + '</li>'
        accessory_text += '</ul>'
        return accessory_text
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

@app.route('/<muscle>1')
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

@app.route('/<muscle>2')
def pretty(muscle):
    accessories = Accessories.query.filter_by(muscle = muscle).order_by(desc(Accessories.name)).all()
    return render_template("index2.html")


@app.route("/")
def home():
    return render_template("index2.html")

if (__name__ == "__main__"):
    app.run(debug=True)