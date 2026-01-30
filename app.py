from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def hello_world():
    return render_template("index.html")

render_template("index.html")

@app.route('/Input', methods=['POST'])
def input():
    data = request.form['name']
    return f'Hello, {data}!' 
@app.route('/home')
def home():
    return render_template("about.html")
