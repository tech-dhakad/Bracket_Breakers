from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for sessions

@app.route("/", methods=["GET", "POST"])
def home():
    # Initialize session variables
    if "count" not in session:
        session["count"] = 0
    if "text" not in session:
        session["text"] = ""

    if request.method == "POST":
        if "increment" in request.form:
            session["count"] += 1
        elif "decrement" in request.form:
            session["count"] -= 1
        elif "text" in request.form:
            session["text"] = request.form["text"]
        return redirect(url_for("home"))  # Redirect to avoid form resubmission

    return render_template("index.html", count=session["count"], text=session["text"])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
