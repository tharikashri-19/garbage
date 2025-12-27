from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "secret"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root123",
    database="civic_db"
)
cursor = db.cursor(dictionary=True)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        cursor.execute(
            "INSERT INTO users (fullname,email,password) VALUES (%s,%s,%s)",
            (request.form['fullname'], request.form['email'], request.form['password'])
        )
        db.commit()
        return redirect('/login')
    return render_template("signup.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        cursor.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (request.form['email'], request.form['password'])
        )
        user = cursor.fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect('/add-complaint')
    return render_template("login.html")

@app.route('/add-complaint', methods=['GET','POST'])
def add_complaint():
    if request.method == 'POST':
        photo = request.files['photo']
        filename = photo.filename
        photo.save(os.path.join(UPLOAD_FOLDER, filename))

        cursor.execute("""
            INSERT INTO complaints
            (user_id,category,description,address,latitude,longitude,photo)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            session['user_id'],
            request.form['category'],
            request.form['description'],
            request.form['address'],
            request.form['latitude'],
            request.form['longitude'],
            filename
        ))
        db.commit()
        return redirect('/')
    return render_template("add_complaint.html")

@app.route('/admin')
def admin():
    cursor.execute("SELECT * FROM complaints")
    complaints = cursor.fetchall()
    return render_template("admin_dashboard.html", complaints=complaints)

@app.route('/update-status/<int:id>', methods=['POST'])
def update_status(id):
    cursor.execute(
        "UPDATE complaints SET status=%s WHERE id=%s",
        (request.form['status'], id)
    )
    db.commit()
    return redirect('/admin')

app.run(debug=True)
