from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from routes.db_config import get_db_connection

auth_bp = Blueprint('auth', __name__)

# DB connection
conn = get_db_connection()
cursor = conn.cursor()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("SELECT * FROM administrators WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        if user:
            print("Login success")
            session['username'] = username
            session['user_id'] = user[0]
            return redirect(url_for('dashboard.home'))
        else:
            print("Login failed")
            flash("Invalid username or password")
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor.execute("INSERT INTO administrators (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        flash("Registration successful! Please login.")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully.")
    return redirect(url_for('auth.login'))
