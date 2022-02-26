from flask import Flask, url_for, redirect

app = Flask(__name__)

@app.route("/")
def home():
    return "this is the main page <h1>Hello!<h1> "

@app.route("/<name>")
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("home"))

if (__name__ == "__main__"):
    app.run()