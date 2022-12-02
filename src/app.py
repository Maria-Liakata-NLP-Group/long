# from flask import Flask
# app = Flask(__name__)
# @app.route('/')
# def home():
#     return 'Flask with docker!'

from webgui.base import app

if __name__ == '__main__':
    app.run_server(debug=True)
