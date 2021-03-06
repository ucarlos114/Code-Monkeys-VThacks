from flask import Flask, flash, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from ProgramCreator import *
# from Conversions import *
from teams import *

app = Flask(__name__)
app.secret_key = "junge"

########################### DATABASES SETUP ############################
db_name = 'exercises.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Accessories(db.Model):
    __tablename__ = "accessories"
    id = db.Column(db.Integer, primary_key=True)
    muscle = db.Column(db.String)
    name = db.Column(db.String)


class Competitors(db.Model):
    __tablename__ = "competitors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    total = db.Column(db.Integer)

    def __init__(self, name, total):
        self.name = name
        self.total = total
########################### END DATABASES SETUP ############################


########## HELPER FUNCTIONS ##########

def compute_teams():    # actually running team generator algorithm
    names = []
    totals = []
    for comp in Competitors.query.all():
        names.append(comp.name)
        totals.append(comp.total)
    teams = arrange_teams(names, totals)
    print(teams)
    return teams


def to_kilo(pound):     # convert pounds into kilos
    return round(0.45359237*float(pound), 1)


def to_pound(kilo):     # convert kilos to pounds
    return round(float(kilo)/0.45359237, 1)

########## END HELPER FUNCTIONS ##########


########## Both lead to default home page ##########
@app.route('/')
def default():
    return redirect(url_for("home"))


@app.route('/home')
def home():
    return render_template("main.html")


########## Show all exercises in database ##########
@app.route('/allexercises')
def all():
    chests = Accessories.query.filter_by(
        muscle="chest").order_by(Accessories.id).all()
    shoulders = Accessories.query.filter_by(
        muscle="shoulders").order_by(Accessories.id).all()
    triceps = Accessories.query.filter_by(
        muscle="triceps").order_by(Accessories.id).all()
    backs = Accessories.query.filter_by(
        muscle="back").order_by(Accessories.id).all()
    biceps = Accessories.query.filter_by(
        muscle="biceps").order_by(Accessories.id).all()
    legs = Accessories.query.filter_by(
        muscle="legs").order_by(Accessories.id).all()

    return render_template("exercises.html", chests=chests, shoulders=shoulders, triceps=triceps,
                           backs=backs, biceps=biceps, legs=legs)

########## About tab ##########


@app.route("/about")
def about():
    return render_template("about.html")

########## Questionnaire required to create a new program ##########


@app.route('/new', methods=["POST", "GET"])
def new():
    if request.method == "POST":
        name = request.form['name']
        days = request.form['days']
        # days not empty and is number between 2 and 6 
        if (not (days.isnumeric() and (2 <= int(days) <= 6))):
            flash("Please enter an amount of days from 2 to 6")
            return render_template("questionnaire.html")
        exp = int(request.form['slider'])

        if (int(exp) > 1 and int(days) < 3):
            flash("For beginner or intermediate programs, minimum days per week is 3")
            return render_template("questionnaire.html")

        # determine exp level as string to display later
        if (exp == 1):
            level = "beginner"
        elif (exp == 2):
            level = "intermediate"
        else:
            level = "advanced"
        # make sure name is not empty, is only letters
        if (len(str(name)) == 0 or not str(name).isalpha()):
            flash("Please enter a valid name")
            return render_template("questionnaire.html")
        return redirect(url_for("process", name=str(name), days=int(days), exp=exp, level=level))

    else:
        return render_template("questionnaire.html")


########## Process the info from questionnaire ##########
@app.route("/program_<name>_<days>days_<level><exp>")
def process(name, days, exp, level):
    prog_create(name, days, exp)
    return render_template("program_done.html", name=name, days=days, level=level)


########## Pound to kilogram calculator ##########
@app.route("/poundtokilo", methods=["POST", "GET"])
def convert():
    if request.method == "POST":
        num = request.form['num']
        conv = request.form['conv-type']
        if (num.isnumeric() and int(num) > 0):
            return redirect(url_for("displayConvert", num=num, conv=conv, drop='kilo'))
        flash("Please enter a number greater than 0")
        return redirect(url_for('convert'))
    else:
        return render_template("convert_main.html", drop='pound')


########## Pound to kilogram result display/restart ##########
@app.route("/display_result_<num>_<conv>", methods=["POST", "GET"])
def displayConvert(num, conv):
    if (str(conv) == 'topound'):
        res = to_pound(num)
        return render_template("converted.html", pound=res, kilo=num, drop='kilo')
    res = to_kilo(num)
    return render_template("converted.html", pound=num, kilo=res, drop='pound')


########## Auto team creator start ##########
@app.route("/team_start", methods=["POST", "GET"])
def teams():
    if request.method == "POST":
        num = request.form['num']
        if (num.isnumeric() and 2 <= int(num) <= 9):
            return redirect(url_for("team_input", num=int(num)))
        flash("Enter a number between 2 and 9", "warning")
        return redirect(url_for('teams'))
    else:
        return render_template("teams.html")


########## Auto team creator competitor input ##########
@app.route("/team_input_<num>_competitors", methods=["POST", "GET"])
def team_input(num):
    if request.method == "POST":
        Competitors.query.delete()  # clear all entries from table
        for i in range(1, int(num) + 1):
            name = request.form['competitor' + str(i)]
            total = request.form['total' + str(i)]
            if (total.isnumeric()):
                comp = Competitors(name, total)
                db.session.add(comp)
                db.session.commit()     # add new entries
            else:
                flash(f"Only enter numbers for totals, {total}")
                return render_template("team_input.html", num=int(num))
        return render_template("display_teams.html", best=compute_teams())

    return render_template("team_input.html", num=int(num))


"""     Run app     """
if (__name__ == "__main__"):
    db.create_all()
    app.run(debug=True)
