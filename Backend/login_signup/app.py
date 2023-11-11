from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from datetime import date
import qrcode
from PIL import Image
import cv2
import geocoder
from geopy.distance import geodesic


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

            student_ip = request.remote_addr  # This will get the student's IP address

            student_location = geocoder.ip(student_ip)
            student_latitude, student_longitude = student_location.latlng

            school_location = (school_latitude, school_longitude)  # School's location
            distance = geodesic(school_location, (student_latitude, student_longitude)).kilometers
            # Define a threshold distance within which the student is considered near the school
            threshold_distance = 10.0  # Adjust this value as needed

            try:
                cursor.execute("INSERT INTO attendance (attendance_name, date, status) VALUES (%s, %s, %s)", (username, date_today, status))
                conn.commit()
            except Exception as e:
                conn.rollback()  # Roll back the transaction on error
                print(f"Error: {e}")
                #added qr code functionality
            qr_code_link = url_for('qr_code', username=username)
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

@app.route('/generate-qr-code/<username>')
def generate_qr_code(username):
    qr = qrcode.QRcode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(username)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black",back_color="white")

    img.save('static/qr_codes/{}.png'.format(username))

    return 'QR code generated: /static/qr_codes/{}.png'.format(username)
@app.route('/qr-code/<username>')
def qr_code(username):
    qr_code_path = '/static/qr_codes/{}.png'.format(username)
    return render_template('qr_code.html', qr_code_path=qr_code_path)
