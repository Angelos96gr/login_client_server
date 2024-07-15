from flask import Flask, render_template, request, redirect
from db_utils import *

specializations = ["Cardiology", "Neuropathy", "Pneumologist"]
simulated_doc_list = [
    {"name": "Dr. Tobias", "address": "Hauzenberger strasse 20", "specialization":specializations[0]},
    {"name": "Dr. Landgrebe", "address": "Laimer Platz 48", "specialization":specializations[2]},
    {"name": "Dr. Poulopoulos", "address": "Griechische strasse 32", "specialization":specializations[1]},
    {"name": "Dr. Jacobsen", "address": "Herzog Heinrich strasse 3", "specialization":specializations[0]},
]


app = Flask(__name__) #defines app.py as a Flask application

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    render_template("index.html")
    return redirect("/")    

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/phonebook")
def show_docs():
    return render_template("doctors_phonebook.html", doctors_list = get_doctors(), users_list = get_users())
    

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        print("User tries to sign up")

        username =  request.form.get("username")
        pwd = request.form.get("pwd")
        
        if register_new_user(username, pwd):
            return redirect("/")        # check user does not exist and create new entry
        else: 
            return redirect("/a")
    return render_template("signup.html")




