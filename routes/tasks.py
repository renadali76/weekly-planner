from flask import Blueprint, render_template, request, redirect, url_for, session

from database import (
    get_task_by_id,
    get_tasks,
    add_task,
    delete_task,
    update_task,
    complete_task,
    get_total_tasks,
    get_completed_tasks,
)

tasks = Blueprint("tasks", __name__)


@tasks.route("/dashboard")
def dashboard():

    total = get_total_tasks(session["user_id"])
    completed = get_completed_tasks(session["user_id"])
    tasks = get_tasks(session["user_id"])
    progress = 0

    if total > 0:
        progress = int((completed / total) * 100)


    return render_template(
    "dashboard.html",
    username=session["username"],
    tasks=tasks,
    total=total,
    completed=completed,
    progress=progress
)


@tasks.route("/add_task", methods=["GET", "POST"])
def add_task_route():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]

        add_task(
            title,
            description,
            due_date,
            priority,
            session["user_id"]
        )

        return redirect(url_for("dashboard"))

    return render_template("add_task.html")


@tasks.route("/delete_task/<int:task_id>")
def delete_task_route(task_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    delete_task(task_id, session["user_id"])

    return redirect(url_for("dashboard"))


@tasks.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        due_date = request.form["due_date"]
        priority = request.form["priority"]

        update_task(
            task_id,
            title,
            description,
            due_date,
            priority,
            session["user_id"]
        )
        return redirect(url_for("dashboard"))
    task = get_task_by_id(task_id, session["user_id"])
    return render_template("edit_task.html", task=task)


@tasks.route("/complete_task/<int:task_id>")
def complete_task_route(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    complete_task(task_id, session["user_id"])
    return redirect (url_for("dashboard"))