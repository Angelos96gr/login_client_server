from flask import Flask, render_template, request, redirect, session, make_response, url_for
from flask_session import Session
from db_utils import *
import random, hashlib


"""
specializations = ["Cardiology", "Neuropathy", "Pneumologist"]
simulated_doc_list = [
    {"name": "Dr. Tobias", "address": "Hauzenberger strasse 20", "specialization":specializations[0]},
    {"name": "Dr. Landgrebe", "address": "Laimer Platz 48", "specialization":specializations[2]},
    {"name": "Dr. Poulopoulos", "address": "Griechische strasse 32", "specialization":specializations[1]},
    {"name": "Dr. Jacobsen", "address": "Herzog Heinrich strasse 3", "specialization":specializations[0]},
]
"""


app = Flask(__name__)  # defines app.py as a Flask application
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)  # defines the flask application to work in the context of sessions


@app.route("/")
def index():
    
    if  (session.get("username") is not None): # user is still logged in
        return render_template("logged_in.html", username=session.get("username"))

    return render_template("index.html")


@app.route("/home", methods=["GET"])
def home():
    render_template("index.html")
    return redirect("/")


@app.route("/about")
def about():
    logged_in = False
    if  (session.get("username") is not None): # user is still logged in
        logged_in = True
    
    return render_template("about.html", logged_in = logged_in, username = session.get("username"))


@app.route("/phonebook")
def show_docs():

    logged_in = False
    if  (session.get("username") is not None): # user is still logged in
        logged_in = True

    return render_template(
        "doctors_phonebook.html", doctors_list=get_doctors(), users_list=get_users(), logged_in=logged_in, username= session.get("username"))


@app.route("/login", methods=["POST"])
def login():

    if request.method == "POST":

        session["username"] = request.form.get("username")
        session["pwd"] = request.form.get("pwd")

        if check_user_exists(session.get("username"), session.get("pwd")):
            resp = make_response(render_template("logged_in.html", username=session.get("username")))
            cookie_value = hashlib.sha256(session["username"].encode('utf-8')).hexdigest() # setting up cookie for tracking which users have logged in
            resp.set_cookie(f"session_custom_{session.get("username").split("@")[0]}", cookie_value) 
            return resp
        else:
            session.clear()
            return render_template(
                "sign_in_up_result.html", action="login", result="unsucessful"

            )


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        print("User tries to sign up")
        result = "unsuccessful"

        session["username"] = request.form.get("username")
        session["pwd"] = request.form.get("pwd")

        if not check_user_exists(session.get("username"), session.get("pwd")):
            register_new_user(session.get("username"), session.get("pwd"))
            result = "succesfull"
        else:
            session.clear()

        return render_template(
            "sign_in_up_result.html", action="registration", result=result
        )

    if request.method == "GET":
        return render_template("signup.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")
