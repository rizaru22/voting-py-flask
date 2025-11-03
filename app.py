from flask import Flask, render_template, request, redirect,url_for,session
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
from secrets import token_hex
from werkzeug.utils import secure_filename
from uuid import uuid4
import os

app=Flask(__name__)
app.secret_key=token_hex(16)
app.config['MYSQL_HOST']='db'
app.config['MYSQL_USER']='db'
app.config['MYSQL_PASSWORD']='db'
app.config['MYSQL_DB']='db'
app.config['UPLOAD_FOLDER']='static/uploads'

ekstensi_yang_diterima={'png','jpg','jpeg','gif'}

mysql=MySQL(app)

def allowed_file(filename):
    #cek apakah ada tanda titik di nama file
    if '.' not in filename:
        return False
    
    # Ambil teks dari file name, kemudian pisahkan berdasarkan titik lalu amil block terakhir
    # misal filename-nya adalah foto.profil.jpg, maka pisahkan lalu ambil jpg
    ekstensi =filename.split('.')[-1].lower()

    return ekstensi in ekstensi_yang_diterima

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verification')
def verification():
    return render_template('verification.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin where username=%s',[username])
        admin=cursor.fetchone()
        cursor.close()

        if admin:
            storedPassword=admin['password']
            bytesStoredPassword=storedPassword.encode('utf-8')
            # kita harus membandingkan password yang disimpan didatabase denga password yang diinput oleh user dari form login
            bytesPassword=password.encode('utf-8')
            if bcrypt.checkpw(bytesPassword,bytesStoredPassword):
                session['id_admin']=admin['id_admin']
                session['nama']=admin['nama']
                session['username']=admin['username']
                return redirect(url_for('pemilu'))
            else:
                return render_template('login.html',error='Password anda salah bro!!')

    return render_template('login.html')

@app.route('/seeder')
def seeder():
    
    username="petugas"
    password="petuga123"
    nama="Petugas Baik Hati"

    bytesPassword=password.encode('utf-8')
    salt=bcrypt.gensalt()
    hashPassword=bcrypt.hashpw(bytesPassword,salt)

    cursor=mysql.connection.cursor()
    cursor.execute('INSERT IGNORE INTO admin (username,password,nama) VALUES (%s,%s,%s)',[username,hashPassword,nama])
    mysql.connection.commit()
    cursor.close()
    return "Berhasil menambahkan admin"


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    
@app.route('/pemilu')
def pemilu():
    if 'id_admin' not in session:
        return redirect(url_for('login'))
    
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM pemilu')
    pemilu=cursor.fetchall()
    cursor.close()

    return render_template('pemilu/index.html', data=pemilu) 

@app.route('/tambah_pemilu',methods=['GET','POST'])
def tambah_pemilu():
    if 'id_admin' not in session:
        return redirect(url_for('login'))
    
    if request.method=='POST':
        nama_pemilu=request.form['nama_pemilu']
        tanggal_mulai=request.form['tanggal_mulai']
        tanggal_selesai=request.form['tanggal_selesai']
        status=request.form['status']
        
        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO pemilu (nama_pemilu, tanggal_mulai,tanggal_selesai,status,id_admin) VALUES (%s,%s,%s,%s,%s)",[nama_pemilu,tanggal_mulai,tanggal_selesai,status,session['id_admin']])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('pemilu'))
    
    return render_template('pemilu/create.html')

@app.route('/edit_pemilu/<int:id>',methods=['GET','POST'])
def edit_pemilu(id):
    if 'id_admin' not in session:
        return redirect(url_for('login'))

    if request.method=='POST':
        nama_pemilu=request.form['nama_pemilu']
        tanggal_mulai=request.form['tanggal_mulai']
        tanggal_selesai=request.form['tanggal_selesai']
        status=request.form['status']
        
        cursor=mysql.connection.cursor()
        cursor.execute("UPDATE pemilu SET nama_pemilu=%s, tanggal_mulai=%s,tanggal_selesai=%s,status=%s,id_admin=%s WHERE id_pemilu=%s",(nama_pemilu,tanggal_mulai,tanggal_selesai,status,session['id_admin'],id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('pemilu'))
    # pilih data dari database
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM pemilu where id_pemilu=%s',[id])
    pemilu=cursor.fetchone()
    return render_template('pemilu/edit.html',data=pemilu)

@app.route('/kelas')
def kelas():
    cursor=mysql.connection.cursor()
    cursor.execute('SELECT * FROM kelas')
    kelas=cursor.fetchall()
    cursor.close()

    return render_template('kelas/index.html', data=kelas)

@app.route('/tambah_kelas',methods=['GET','POST'])
def tambah_kelas():
    if request.method=='POST':
        kode_kelas=request.form['kode_kelas']
        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO kelas (kode_kelas) VALUES (%s)',[kode_kelas])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('kelas'))
    return render_template('/kelas/create.html')

@app.route('/voters')
def voters():
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT voters.id_voter,voters.nama,kelas.kode_kelas FROM voters JOIN kelas ON kelas.id_kelas=voters.id_kelas')
    voters=cursor.fetchall()
    cursor.close()
    return render_template('/voters/index.html',data=voters)

@app.route('/tambah_pemilih',methods=['GET','POST'])
def tambah_voters():
    if request.method=='POST':
        nama=request.form['nama']
        id_kelas=request.form['id_kelas']
        cursor=mysql.connection.cursor()
        cursor.execute('INSERT INTO voters (nama,id_kelas) values(%s,%s)',[nama,id_kelas])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('voters'))

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM kelas')
    kelas=cursor.fetchall()
    cursor.close()
    return render_template('/voters/create.html', data_kelas=kelas)

@app.route('/edit_pemilih/<int:id>', methods=['GET','POST'])
def edit_voters(id):
    if request.method=='POST':
        nama=request.form['nama']
        id_kelas=request.form['id_kelas']
        cursor=mysql.connection.cursor()
        cursor.execute('UPDATE voters SET nama=%s, id_kelas=%s WHERE id_voter=%s',[nama,id_kelas,id])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('voters'))

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM voters WHERE id_voter=%s",[id])
    voter=cursor.fetchone()
    cursor.execute("SELECT * FROM kelas")
    kelas=cursor.fetchall()
    cursor.close()
    return render_template('/voters/edit.html', data=voter,data_kelas=kelas)

@app.route('/hapus_pemilih/<int:id>',methods=['POST'])
def hapus_voters(id):
    cursor=mysql.connection.cursor()
    cursor.execute("DELETE FROM voters WHERE id_voter=%s",[id])
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('voters'))

@app.route('/kandidat')
def kandidat():
    # pengecekan login
    if 'id_admin' not in session:
        return redirect(url_for('login'))
    
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM candidates')
    kandidat=cursor.fetchall()
    cursor.close()
    return render_template('kandidat/index.html',data=kandidat)

@app.route('/tambah_kandidat',methods=['GET','POST'])
def tambah_kandidat():
    if 'id_admin' not in session:
        return redirect(url_for('login'))
    
    if request.method=='POST':
        nama=request.form['nama']
        visi=request.form['visi']
        misi=request.form['misi']
        id_pemilu=request.form['id_pemilu']
        foto=request.files['foto']

        if foto and allowed_file(foto.filename):
            filename=f"{uuid4().hex}_{secure_filename(foto.filename)}"
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            foto.save(filepath)

        cursor=mysql.connection.cursor()
        cursor.execute("INSERT INTO candidates (nama,visi,misi,id_pemilu,foto) values (%s,%s,%s,%s,%s)",[nama,visi,misi,id_pemilu,filename])
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('kandidat'))
    
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM pemilu WHERE status='T'")
    pemilu=cursor.fetchall()
    cursor.close()
    return render_template('kandidat/create.html',data=pemilu)

@app.route('/edit_kandidat/<int:id>',methods=['GET','POST'])
def edit_kandidat(id):
    if 'id_admin' not in session:
        return redirect(url_for('login'))
    
    if request.method=='POST':
        nama=request.form['nama']
        visi=request.form['visi']
        misi=request.form['misi']
        id_pemilu=request.form['id_pemilu']
        foto=request.files['foto']

        cursor=mysql.connection.cursor()
        if foto and allowed_file(foto.filename):
            filename=f"{uuid4().hex}_{secure_filename(foto.filename)}"
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],filename)
            foto.save(filepath)
            cursor.execute("UPDATE candidates SET nama=%s,visi=%s,misi=%s,id_pemilu=%s,foto=%s WHERE id_candidate=%s",[nama,visi,misi,id_pemilu,filename,id])
        else:
            cursor.execute("UPDATE candidates SET nama=%s,visi=%s,misi=%s,id_pemilu=%s WHERE id_candidate=%s",[nama,visi,misi,id_pemilu,id])

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('kandidat'))
    
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM pemilu WHERE status='T'")
    pemilu=cursor.fetchall()

    cursor.execute("SELECT * FROM candidates WHERE id_candidate=%s",[id])
    kandidat=cursor.fetchone()
    cursor.close()

    return render_template('kandidat/edit.html',data=pemilu,kandidat=kandidat)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)