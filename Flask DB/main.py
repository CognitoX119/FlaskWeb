from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql

app = Flask (__name__)
app.secret_key = 'your_secret_key'
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'flask'
}

def get_db_connection():
    return pymysql.connect(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database']
    )

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return render_template('homepage.html')
        else:
            flash('Invalid credentials. Please try again.')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash('Username already exists.')
        else:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            flash('Registration successful!')
            return redirect(url_for('login'))
        conn.close()
    return render_template('signup.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user:
            cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))
            conn.commit()
            flash('Password updated successfully!')
            return redirect(url_for('login'))
        else:
            flash('Username not found.')
        conn.close()
    return render_template('forgot_password.html')

@app.route('/homepage')
def homepage():
    return render_template('login.html')

@app.route('/trending')
def trending():
    return render_template('trending.html')

@app.route('/beauty')
def beauty():
    return render_template('beauty.html')

@app.route('/vouchers')
def vouchers():
    return render_template('vouchers.html')

@app.route('/rewards')
def rewards():
    return render_template('rewards.html')

if __name__ == '__main__':
    app.run(debug=True)