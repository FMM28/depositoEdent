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
    page = int(request.args.get('page', 1))
    search_query = request.args.get('search', '')
    selected_id = request.args.get('id')
    selected_category = request.args.get('category')

    conn = get_db_connection()
    cursor = conn.cursor()

    if search_query != '':
        offset = (page - 1) * 10
        search_query = search_query.replace(' ','%')
        
        query = '''SELECT * FROM productos WHERE nombre LIKE ? ORDER BY nombre LIMIT 10 OFFSET ?'''
        cursor.execute(query, (f'%{search_query}%', offset))
        products = cursor.fetchall()

        cursor.execute('SELECT COUNT(*) FROM products WHERE nombre LIKE ?', (f'%{search_query}%',))
        total_count = cursor.fetchone()[0]
        
        total_pages = (total_count // 10) + (1 if total_count % 10 > 0 else 0)
    
    elif selected_category:
        offset = (page - 1) * 10
        
        query = '''SELECT * FROM productos WHERE categoria = ? ORDER BY nombre LIMIT 10 OFFSET ?'''
        cursor.execute(query, (selected_category, offset))
        categorias = cursor.fetchall()

        cursor.execute('SELECT COUNT(*) FROM products WHERE nombre LIKE ?', (f'%{search_query}%',))
        total_count = cursor.fetchone()[0]
        
        total_pages = (total_count // 10) + (1 if total_count % 10 > 0 else 0)
    
    else:
        offset = (page - 1) * 12
        
        query = '''SELECT * FROM categorias ORDER BY nombre LIMIT 10 OFFSET ?'''
        cursor.execute(query, (offset,))
        products = cursor.fetchall()

        cursor.execute('SELECT COUNT(*) FROM categorias')
        total_count = cursor.fetchone()[0]

        total_pages = (total_count // 12) + (1 if total_count % 12 > 0 else 0)
    
    selected_product = None
    if selected_id:
        cursor.execute('SELECT * FROM products WHERE id = ?', (selected_id,))
        selected_product = cursor.fetchone()

    conn.close()

    return render_template("inventario.html",
                           products=products,
                           page=page,
                           total_pages=total_pages,
                           search_query=search_query,
                           selected_product=selected_product,
                           selected_category=selected_category,
                           categorias=categorias)

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