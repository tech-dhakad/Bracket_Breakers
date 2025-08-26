from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/", methods=["GET", "POST"])
def home():
    if "tasks" not in session:
        session["tasks"] = []

    if request.method == "POST":
        if "add" in request.form:
            new_task = request.form.get("task")
            if new_task.strip():
                session["tasks"].append(new_task)
                session.modified = True
        elif "remove" in request.form:
            index = int(request.form.get("remove"))
            session["tasks"].pop(index)
            session.modified = True

        return redirect(url_for("home"))

    return render_template("index.html", tasks=session["tasks"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
