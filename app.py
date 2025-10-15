from flask import Flask, render_template, request, redirect,url_for,session
from flask_mysqldb import MySQL,MySQLdb

app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='db_pemilu_osis'

mysql=MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verification')
def verification():
    return render_template('verification.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/pemilu')
def pemilu():
    return render_template('pemilu/index.html')

@app.route('/kelas')
def kelas():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM kelas')
    kelas=cursor.fetchall()
    cursor.close()

    return render_template('kelas/index.html', data=kelas)

if __name__=='__main__':
    app.run(debug=True)