from flask import Flask, render_template

from routes.auth import auth
from routes.tasks import tasks

app = Flask(__name__)
app.secret_key = "your_secret_key"

app.register_blueprint(auth)
app.register_blueprint(tasks)


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)