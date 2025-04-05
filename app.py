from flask import Flask, render_template, request, send_file
from generator_interaction_label import generer_avatar
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    avatar_generated = False
    if request.method == "POST":
        couleur = request.form.get("couleur")
        etat = request.form.get("etat")
        element = request.form.get("element")
        interaction = request.form.get("interaction")

        # 调用角色生成函数
        img = generer_avatar(couleur, etat, element, interaction)
        img_path = os.path.join("static", "mon_avatar.png")
        img.save(img_path)
        avatar_generated = True

    return render_template("index.html", avatar_generated=avatar_generated)

@app.route("/avatar")
def get_avatar():
    return send_file("static/mon_avatar.png", mimetype="image/png")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



