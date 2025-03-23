from flask import Flask, render_template, request
from generator import generer_avatar
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        couleur = request.form.get("couleur")
        emotion = request.form.get("emotion")
        element = request.form.get("element")
        generer_avatar(couleur, emotion, element)
    return render_template("index.html")

if __name__ == "__main__":
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)
