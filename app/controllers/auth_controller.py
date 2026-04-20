from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from app.config import get_db_connection
import bcrypt

# Define the blueprint
auth = Blueprint('auth', __name__)

# --- REGISTER ---
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Use .form.get to avoid KeyErrors if a field is missing
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            return "All fields are required", 400

        # Hashing the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            # Ensure the table name 'users' matches your DB
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, hashed_password))
            conn.commit()
            cursor.close()
            conn.close()
            
            # Use 'auth.login' to reference the route within this blueprint
            return redirect(url_for('auth.login'))
        except Exception as e:
            return f"Error during registration: {str(e)}"

    # If GET request, show the register page
    return render_template('register.html')

# --- LOGIN ---
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            conn = get_db_connection()
            # Note: dictionary=True is specific to mysql-connector-python
            # If using flask_mysqldb, you'd access by index like user[3]
            cursor = conn.cursor(dictionary=True) 
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                # Setting session variables
                session.permanent = True # Keep them logged in for the session
                session['user_id'] = user['id']
                session['username'] = user['username']
                
                # Redirect to 'dashboard' route in your run.py
                return redirect(url_for('dashboard')) 
            
            return "Invalid email or password", 401
            
        except Exception as e:
            return f"Database Error: {str(e)}"

    # If GET request, show the login page
    return render_template('login.html')

# --- LOGOUT ---
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))