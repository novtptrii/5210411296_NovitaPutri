from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL


app = Flask(__name__,template_folder='template')

app.secret_key='!@#$%'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='flaskmysql'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'inpEmail' in request.form and 'inpPass' in request.form:
        email = request.form['inpEmail']
        passwd = request.form['inpPass']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usser where email = %s and pasword = %s", (email, passwd))
        result = cur.fetchone()
        if result:
            session['is_logged_in'] = True
            session['username'] = result[1]
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
@app.route('/home')
def home():
    if 'is_logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM usser')
        data = cur.fetchall()
        cur.close()
        return render_template('home.html', usser=data )
    else:
        return redirect(url_for('login'))

@app.route("/registrasi",methods=["GET","POST"])
def regis():
    if request.method == 'GET':
        return render_template('registrasi.html')
    else:
        nama=request.form['nama']
        email=request.form['email']
        pasword=request.form['pw']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usser(nama,email,pasword) VALUES(%s,%s,%s)",(nama,email,pasword))
        registrasi = mysql.connection.commit()
        cur.close()
        session['nama'] = request.form['nama']
        session['password'] = request.form['pw']
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('is_logged_out',None)
    session.pop('username', None)
    return redirect(url_for('login'))
if __name__== '__main__':
    app.run(debug=True)