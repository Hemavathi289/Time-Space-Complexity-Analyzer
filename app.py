from flask import Flask, render_template, request
from analyzer import analyze_code

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    hints = []
    code = ""

    if request.method == "POST":

        code = request.form["code"]
        result, hints = analyze_code(code)

    return render_template("index.html", result=result, hints=hints, code=code)


if __name__ == "__main__":
    app.run(debug=True)