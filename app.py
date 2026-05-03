from flask import Flask, render_template, request, redirect, session
from database import create_tables, get_connection

app = Flask(__name__)
app.secret_key = "daily_tracker_secret_key"

create_tables()

@app.route("/")
def home():
    connection = get_connection()
    active_activities = connection.execute(
        "SELECT * FROM activities WHERE completed = 0"
    ).fetchall()

    completed_activities = connection.execute(
        "SELECT * FROM activities WHERE completed = 1"
    ).fetchall()
    connection.close()
    role = session.get("role", "user")
    return render_template(
    "index.html",
    active_activities=active_activities,
    completed_activities=completed_activities,
    role=role
)

@app.route("/add", methods=["POST"])
def add_activity():
    activity_name = request.form.get("activity_name")

    if activity_name:
        connection = get_connection()
        connection.execute(
            "INSERT INTO activities (name) VALUES (?)",
            (activity_name,)
        )
        connection.commit()
        connection.close()

    return redirect("/")

@app.route("/complete/<int:id>", methods=["POST"])
def complete_activity(id):
    connection = get_connection()
    connection.execute(
        "UPDATE activities SET completed = 1 WHERE id = ?",
        (id,)
    )
    connection.commit()
    connection.close()

    return redirect("/")

@app.route("/set-role/<role>")
def set_role(role):
    if role in ["user", "admin"]:
        session["role"] = role

    return redirect("/")

@app.route("/delete/<int:id>", methods=["POST"])
def delete_activity(id):
    if session.get("role") != "admin":
        return redirect("/")

    connection = get_connection()
    connection.execute(
        "DELETE FROM activities WHERE id = ?",
        (id,)
    )
    connection.commit()
    connection.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)