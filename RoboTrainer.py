from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db_name = 'exercises.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Accessories(db.Model):
    __tablename__ = "accessories"
    id = db.Column(db.Integer, primary_key=True)

@app.route('/muscle')
def get_exercises(muscle):
    Accessories.query.filter_by(muscle)



@app.route("/")
def home():
    return render_template("index2.html")

if (__name__ == "__main__"):
    app.run(debug=True)