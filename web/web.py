from flask import Flask, render_template, redirect, url_for, request

import field_2, line_type_distribution, line_vs_length, outcome_distribution, shot_position_distribution, shot_type_distribution, strenght_weakness

app = Flask(__name__)

@app.route("/<ans>")
def answer(ans):
    return render_template("result.html")

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        overs = request.form["overs"]
        matrix = request.form["matrix"]
        if matrix == "1":
            line = request.form["line"]
            length = request.form["length"]
            field_2.field(overs, line, length)
        elif matrix == "2":
            line_type_distribution.line_type(overs)
        elif matrix == "3":
            line_vs_length.line_length(overs)
        elif matrix == "4":
            outcome_distribution.outcome(overs)
        elif matrix == "5":
            shot_position_distribution.shot_position(overs)
        elif matrix == "6":
            shot_type_distribution.shot_type(overs)
        elif matrix == "7":
            strenght_weakness.strength_weakness(overs)
        else:
            print("Invalid input\n")
        
        
        #return redirect(url_for("answer", ans=matrix))
        return redirect(url_for("home"))

    else:
        return render_template("index.html")
    


if __name__ == "__main__":
    app.run(debug=True)