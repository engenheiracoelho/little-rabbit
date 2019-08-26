from flask import (
        redirect, render_template, request, session, url_for, Flask,jsonify
)
import json
import bson

from flask_httpauth import HTTPBasicAuth
from bson.objectid import ObjectId

from pprint import pprint

application = Flask(__name__)
auth = HTTPBasicAuth()

# set the secret key.  keep this really secret:
application.secret_key = '2887157sdhurywnadpakpefli5bf27c9998f6edeaa960c9255'
#-- oAuth Operations --#
@auth.get_password
def get_pw(username):

    user = People.find_one({"login":username})
    if user is not None:
        return user['password']
    return None
    
@application.route("/")
#@auth.login_required
def index():
    return render_template('index.html')

@application.route("/index.html")
#@auth.login_required
def home():
    return render_template('index.html')


@application.route("/face.html")
#@auth.login_required
def face():
    return render_template('face.html')

@application.route("/elements.html")
#@auth.login_required
def elements():
    return render_template('elements.html')

@application.route("/generic.html")
#@auth.login_required
def generic():
    return render_template('generic.html')

if __name__ == "__main__":
    application.run(host="0.0.0.0", port='8080')
