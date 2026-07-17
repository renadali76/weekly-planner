from flask import Flask, render_template, request
from database import add_user
from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.route("/")

def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register" , methods = ["GET" , "POST"])
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
        return "Registration successful!"


    return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)