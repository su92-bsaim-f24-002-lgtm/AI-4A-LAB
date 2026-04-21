from flask import Flask, render_template, request
from textblob import TextBlob

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    sentiment = None
    text = ""

    if request.method == "POST":
        text = request.form["text"]
        analysis = TextBlob(text)
        polarity = analysis.sentiment.polarity

        if -0.3 <= polarity <= 0.3:
            sentiment = "Neutral 😐"
        elif polarity > 0.3:
            sentiment = "Positive 😊"
        else:
            sentiment = "Negative 😡"

    return render_template("index.html", sentiment=sentiment, text=text)

if __name__ == "__main__":
    app.run(debug=True)