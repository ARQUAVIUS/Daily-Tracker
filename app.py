from flask import Flask, render_template, request, redirect

app = Flask(__name__)

activities = []

@app.route("/")
def home():
    return render_template("index.html", activities=activities)

@app.route("/add", methods=["POST"])
def add_activity():
    activity_name = request.form.get("activity_name")

    if activity_name:
        activities.append(activity_name)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)