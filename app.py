'''
from flask import Flask

app = Flask(__name__)

@app.route("/ola")
def hello():
    from flask import request, jsonify, render_template
    return "Hello from FastCGI via IIS - Lucas!"
if __name__ == "__main__":
 app.run()

'''



import flask
from flask import Flask
from flask import request, jsonify, render_template
import sqlite3
#from flask_sslify import SSLify
import datetime
from datetime import datetime
import time
import html
import logging



#from flask_cors import CORS
app = flask.Flask(__name__)
dbpath='/home/nayara/Documentos/api-dados-extraidos-sesdf/'
dbname='dados-extraidos-covid19-sesdf.db'
global db
db=dbpath+dbname
#CORS(app)
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d




@app.route("/apiv2")
def hello():
    return "<h1>Distant Reading Archive</h1><p>A prototype API for distant reading of science fiction novels.</p>"
    #return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/apiv2/regiao/all', methods=['GET'])
def api_all():
    print("!!!!!!!!")
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_data = cur.execute('SELECT * FROM \"dados-extraidos-covid19-sesdf\";').fetchall()
    return jsonify(all_data)
    #return render_template('site.html')



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/apiv2/regiao/', methods=['GET'])
def api_filtro():
    query_parameters = request.args;
    #cpf = query_parameters.get('cpf')
    dataExtracao = query_parameters.get('dataExtracao')
    if(dataExtracao):
        dataExtracao=html.unescape(dataExtracao)
    print(dataExtracao)
    regiao = query_parameters.get('regiao')
    if(regiao):
        regiao=html.unescape(regiao)
    print(regiao)
    #conta1mt5 = query_parameters.get('conta1mt5')
    #conta2mt5 = query_parameters.get('conta2mt5')
    query = "SELECT * FROM \"dados-extraidos-covid19-sesdf\" WHERE"
    to_filter = []
    #if (cpf):
     #   query += ' cpf=? AND'
     #   to_filter.append(cpf)
    if (dataExtracao):
        query += ' dataExtracao=? AND'
        to_filter.append(dataExtracao)
    if (regiao):
        query += ' regiao=? AND'
        to_filter.append(regiao)
    #if idcompra:
    #    query += ' idcompra=? AND'
    #   to_filter.append(idcompra)
    #if conta1mt5 and (not conta2mt5):
    #    query += ' conta1mt5=? AND'
    #    to_filter.append(conta1mt5)
    #if conta2mt5 and (not conta1mt5):
    #    query += ' conta2mt5=? AND'
    #    to_filter.append(conta2mt5)
    #if not (cpf or email or idcompra or conta1mt5 or conta2mt5):
    #    return page_not_found(404)
    if not (regiao or dataExtracao):
        return page_not_found(404)
    query = query[:-4] + ';'
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, to_filter).fetchall()
    results=flask.jsonify(results)
    #results.headers.add('Access-Control-Allow-Origin', '*')
    return results




@app.route('/apiv2/regiao/list', methods=['GET'])
def api_list():
    print("!!!!!!!!2")
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_data = cur.execute('SELECT regiao,COUNT(DISTINCT regiao) FROM \"dados-extraidos-covid19-sesdf\" GROUP BY regiao;').fetchall()
    return jsonify(all_data)
    #return render_template('site.html')

@app.route('/apiv2/regiao/maxincid', methods=['GET'])
def api_maxinc():
    conn = sqlite3.connect(db)
    conn.row_factory = dict_factory
    cur = conn.cursor()
    max_data = cur.execute('SELECT MAX(incidencia) FROM \"dados-extraidos-covid19-sesdf\";').fetchone()
    max_obit = cur.execute('SELECT MAX(obitos) FROM \"dados-extraidos-covid19-sesdf\";').fetchone()
    maximum = max_data['MAX(incidencia)']
    interval = int(max_data['MAX(incidencia)']/5)
    maxObitos = max_obit['MAX(obitos)']
    intervalObitos = int(max_obit['MAX(obitos)']/5)
    newDic= {
        "num":[interval, 2*interval, 3*interval, 4*interval],
        "obitos":[intervalObitos, 2*intervalObitos, 3*intervalObitos, 4*intervalObitos]}
    return jsonify(newDic)


def add_headers_to_fontawesome_static_files(response):
    """
    Fix for font-awesome files: after Flask static send_file() does its
    thing, but before the response is sent, add an
    Access-Control-Allow-Origin: *
    HTTP header to the response (otherwise browsers complain).
    """
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response





#SSL PRECISA DO pyOpenSSL instalado
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host='0.0.0.0', port=5003)
    app.after_request(add_headers_to_fontawesome_static_files)
    #app.run(ssl_context='adhoc')


