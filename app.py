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
    return render_template('login.html')

@application.route("/index.html")
@auth.login_required
def home():
    return render_template('index.html')

@application.route("/destinos.html")
@auth.login_required
def destinos():
    return render_template('destinos.html')

if __name__ == "__main__":
    application.run(host="0.0.0.0", port='8080')
