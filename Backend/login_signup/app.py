from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from datetime import date

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
conn = psycopg2.connect(
    database="bsuh3", user="bsuh3", password="bsuh3", host="localhost", port="5432"
)
cursor = conn.cursor()

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
        except Exception as e:
            conn.rollbacK()
            print(f"error: {e}")

        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            session['username'] = username
            return redirect(url_for('home'))

        return "Invalid login credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/mark-attendance', methods=['GET', 'POST'])
def mark_attendance():
    if 'username' in session:
        if request.method == 'POST':
            username = session['username']
            date_today = date.today()
            status = request.form.get('status', False)

            try:
                cursor.execute("INSERT INTO attendance (attendance_name, date, status) VALUES (%s, %s, %s)", (username, date_today, status))
                conn.commit()
            except Exception as e:
                conn.rollback()  # Roll back the transaction on error
                print(f"Error: {e}")

        return render_template('mark_attendance.html')
    return redirect(url_for('login'))


@app.route('/view-attendance')
def view_attendance():
    if 'username' in session:
        attendance_username = session['username']
        cursor.execute("SELECT * FROM attendance WHERE attendance_name = %s ORDER BY date DESC", (attendance_username,))
        records = cursor.fetchall()
        return render_template('view_attendance.html', records=records)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)