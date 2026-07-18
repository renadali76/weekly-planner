from flask import Flask, render_template, request, session, redirect , url_for
from database import add_user, get_user_by_email, add_task, get_tasks
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "BadooryisaDoctor!23"
@app.route("/")

def home():
    return render_template("home.html")

@app.route("/login", methods = ["GET", "POST"])
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
            return redirect(url_for("dashboard"))
        
        return "Inccorect password."
    
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
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    return render_template("dashboard.html" , username=session["username"])

@app.route("/add_task", methods=["GET", "POST"])
def add_task_route():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method =="POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]

        add_task(
            title , description, due_date, priority, session["user_id"])
        
        return redirect(url_for("dashboard"))
    return render_template("add_task.html")
if __name__ == "__main__":
    app.run(debug=True)