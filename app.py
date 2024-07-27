from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    make_response,
    url_for,
)
from flask_session import Session
from db_utils import *
import hashlib


app = Flask(__name__)  # defines app.py as a Flask application
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
Session(app)  # defines the flask application to work in the context of sessions


@app.route("/")
def index():

    if session.get("username") is not None:  # user is still logged in
        return render_template("logged_in.html", username=session.get("username"))

    return render_template("index.html")


@app.route("/home", methods=["GET"])
def home():
    render_template("index.html")
    return redirect("/")


@app.route("/about")
def about():
    logged_in = False
    if session.get("username") is not None:  # user is still logged in
        logged_in = True

    return render_template(
        "about.html", logged_in=logged_in, username=session.get("username")
    )


@app.route("/phonebook")
def show_docs():

    logged_in = False
    if session.get("username") is not None:  # user is still logged in
        logged_in = True

    return render_template(
        "doctors_phonebook.html",
        doctors_list=get_doctors(),
        users_list=get_users(),
        logged_in=logged_in,
        username=session.get("username"),
    )


@app.route("/login", methods=["POST"])
def login():

    if request.method == "POST":

        session["username"] = request.form.get("username")
        session["pwd"] = request.form.get("pwd")

        if check_user_exists(session.get("username"), session.get("pwd")):
            resp = make_response(
                render_template("logged_in.html", username=session.get("username"))
            )

            # setting up cookie for tracking which users have logged in
            cookie_value = hashlib.sha256(
                session["username"].encode("utf-8")
            ).hexdigest()
            resp.set_cookie(
                f'session_custom_{session.get("username").split("@")[0]}', cookie_value
            )
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
            register_new_user(session.get("username"), session["pwd"])
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


@app.route("/delete")
def delete():
    print(f'Deleting user {session.get("username")}')
    delete_user(session.get("username"), session.get("pwd"))
    session.clear()
    return redirect("/")


@app.route("/book_appointment")
def book():
    # ToDo to suppot booking apppointments with one of the registered users
    return redirect("/phonebook")


@app.route("/register_doc", methods=["GET", "POST"])
def register_doc():
    if request.method == "GET":
        logged_in = False
        if session.get("username") is not None:  # user is still logged in
            logged_in = True

            # capitalize only first letter
        return render_template("register_doc.html", logged_in=logged_in)
    else:
        result = "unsuccessful"
        session["full_name"] = " ".join(
            [request.form.get("first_name"), request.form.get("last_name")]
        )
        session["address"] = " ".join(
            [
                request.form.get("address_street"),
                str(request.form.get("address_postal")),
            ]
        )
        session["specialization"] = request.form.get("specialization")
        if register_new_doctor(
            session["full_name"],
            session["address"],
            session["specialization"],
            session.get("username"),
        ):
            result = "successful"

        return render_template(
            "sign_in_up_result.html", action="registration", result=result
        )
