from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from database import add_user, get_user_by_email

auth = Blueprint("auth", __name__)




@auth.route("/login", methods = ["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)

        if user is None:
            return "Email not found"
        if check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("tasks.dashboard"))
        
        return "Inccorect password."
    
    return render_template("login.html")


@auth.route("/register" , methods = ["GET" , "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]

        password = request.form["password"]
        hashed_password = generate_password_hash(password)

        print(username)
        print(email)
        print(password)
        add_user(username, email, hashed_password)
        return redirect(url_for("auth.login"))


    return render_template("register.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))