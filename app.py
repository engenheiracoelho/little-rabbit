from flask import (
        redirect, g, render_template, request, session, url_for, Flask,jsonify
)
import json
import bson

from flask_httpauth import HTTPBasicAuth
from bson.objectid import ObjectId
from pprint import pprint
from mysql.connector import MySQLConnection, Error

application = Flask(__name__)
auth = HTTPBasicAuth()

# set the secret key.  keep this really secret:
application.secret_key = '2887157sdhurywnadpakpefli5bf27c9998f6edeaa960c9255'

#--Mysql--#
db_config = {
    'user': 'root',
    'password': 'imagine123',
    'host': 'localhost',
    'database': 'my',
    'raise_on_warnings': True,
}

#-- oAuth Operations --#
@auth.get_password
def get_pw(username):

    nome = []
    senha = []

    t = (username,)

    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()
    cursor.execute("SELECT * FROM people WHERE nome=%s", t)

    coluna = [tupla for tupla in cursor.fetchall()]
    for coluna in coluna:
        nome = coluna[1]
        senha = coluna[2]

    g.db.commit()
    cursor.close()
    g.db.close()
    if nome==[] and senha==[]:
        return None 
    else:
        return senha
    
@application.route("/")
#@auth.login_required
def index():
    return render_template('login.html')

@application.route("/index.html")
@auth.login_required
def home():
    resultado = []
    g.db = MySQLConnection(**db_config)
    cursor = g.db.cursor()

    consulta = "SELECT nome,sobrenome,telefone,email FROM people where nome=%s"

    cursor.execute(consulta,(auth.username(),))

    for (nome,sobrenome,telefone,email) in cursor:
        resultado.append({'nome': nome,'sobrenome': sobrenome, 'telefone':telefone, 'email':email })

    g.db.commit()
    cursor.close()
    g.db.close()
    return render_template('index.html', user=resultado)

@application.route("/destinos.html")
@auth.login_required
def destinos():
    return render_template('destinos.html')

#--People--#
@application.route('/inserir.html', methods=('GET', 'POST'))
def inserir():
    try:    
        nome = request.form['nome']
        senha = request.form['senha']
        sobrenome = request.form['sobrenome']
        telefone = request.form['telefone']
        email = request.form['email']

        g.db = MySQLConnection(**db_config)
        cursor = g.db.cursor()

        consulta = "INSERT INTO people (nome,senha,sobrenome,telefone,email) VALUES (%s,%s,%s,%s,%s)"
        dados = (nome,senha,sobrenome,telefone,email) 
        print(dados)
        cursor.execute(consulta, dados)
        g.db.commit()
        cursor.close()
        g.db.close()

        return render_template('login.html', title='Adicionar Contato')
    
    except:
        return render_template('inserir.html', title='Adicionar Contato')



if __name__ == "__main__":
    application.run(host="0.0.0.0", port='8080')
