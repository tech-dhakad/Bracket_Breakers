from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def profile():
    user = {
        "name": "Arpita Sharma",
        "age": 19,
        "bio": "A passionate learner who loves coding",
        "image": "https://via.placeholder.com/100"
    }
    return render_template("profile_card.html", user=user)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
