from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# API route to get joke
@app.route('/get-joke')
def get_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    data = response.json()

    joke = data['setup'] + " - " + data['punchline']
    return jsonify({'joke': joke})

if __name__ == '__main__':
    app.run(debug=True)