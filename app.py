from flask import Flask, render_template, request, redirect
from database import create_tables, get_connection

app = Flask(__name__)

create_tables()

@app.route("/")
def home():
    connection = get_connection()
    activities = connection.execute("SELECT * FROM activities").fetchall()
    connection.close()

    return render_template("index.html", activities=activities)

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

if __name__ == "__main__":
    app.run(debug=True)