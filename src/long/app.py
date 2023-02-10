# from flask import Flask
# app = Flask(__name__)
# @app.route('/')
# def home():
#     return 'Flask with docker!'

from webgui.base import app

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
    # , dev_tools_ui=False)
    # app.enable_dev_tools(
    #     dev_tools_ui=False,
    #     dev_tools_serve_dev_bundles=False,
    # )
    # app.run_server(debug=False)
