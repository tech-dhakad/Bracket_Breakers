from flask import Flask, render_template

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 75000, "img": "https://via.placeholder.com/150"},
    {"id": 2, "name": "Smartphone", "price": 35000, "img": "https://via.placeholder.com/150"},
    {"id": 3, "name": "Headphones", "price": 2000, "img": "https://via.placeholder.com/150"}
]

@app.route("/")
def home():
    return render_template("index.html", products=products)

if __name__ == "__main__":
    app.run(debug=True)
