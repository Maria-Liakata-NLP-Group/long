from flask import Flask

app = Flask(__name__)

@app.route('/flask')
def home():
    return 'Flask with docker!'
