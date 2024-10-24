from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from sqlite3 import *
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def get_db_connection():
    conn = connect('./DB/db.db')
    conn.row_factory = Row
    return conn

@app.route('/',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = get_db_connection()
        user = cursor.execute('SELECT * from usuarios where username = ?',(username,)).fetchone()
        cursor.close()

        if user and password==user['password']:
            session['username'] = username
            session['role'] = user['role']
            session['user_id'] = user['id_usuario']
            return redirect(url_for('home'))
        else:
            flash('Usuario o Contraseña incorrecto')
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')
    
@app.route('/ventas')
def ventas():
    return render_template('base.html')

@app.route('/inventario')
def inventario():
    return render_template('base.html')

@app.route('/pedidos')
def pedidos():
    return render_template('base.html')

@app.route('/administracion')
def administracion():
    return render_template('base.html')

@app.route('/facturas')
def facturas():
    return render_template('base.html')

@app.route('/estadisticas')
def estadisticas():
    return render_template('base.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

app.run(host='0.0.0.0',port=3000)