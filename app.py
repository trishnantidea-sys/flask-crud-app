from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super_secret_key_gudang'
app.config['DATABASE'] = os.path.join(app.instance_path, 'db_gudang_flask.db')

# Ensure the instance folder exists
os.makedirs(app.instance_path, exist_ok=True)

def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with app.app_context():
        db = get_db()
        # Users table
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                full_name TEXT,
                email TEXT,
                gender TEXT,
                age INTEGER,
                occupation TEXT,
                city TEXT,
                phone TEXT
            )
        ''')
        # Packages table
        db.execute('''
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resi TEXT UNIQUE NOT NULL,
                sender TEXT NOT NULL,
                sender_phone TEXT,
                receiver TEXT NOT NULL,
                receiver_phone TEXT,
                destination_address TEXT,
                category TEXT,
                weight REAL,
                shipping_date TEXT,
                shipping_type TEXT,
                estimation TEXT,
                fare INTEGER
            )
        ''')
        
        # Seed initial data if tables are empty
        user_count = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        if user_count == 0:
            # Seed users from database.py
            initial_users = [
                ("admin123", "Admin@123", "Admin Utama", "admin@mail.com", "Male", 30, "Manager", "Jakarta", "081234567890"),
                ("dea2026", "Dea#2026", "Dea Trishnanti", "dea@gmail.com", "Female", 25, "Staff Gudang", "Bandung", "085678901234"),
                ("lauzia99", "Lauzia@99", "Lauzia Fadhila", "lauzia@yahoo.com", "Female", 23, "Admin", "Surabaya", "087654321098"),
                ("user456", "User@456", "Budi Santoso", "user@hotmail.com", "Male", 28, "Kurir", "Yogyakarta", "089012345678")
            ]
            for u in initial_users:
                db.execute(
                    "INSERT INTO users (username, password, full_name, email, gender, age, occupation, city, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (u[0], generate_password_hash(u[1]), u[2], u[3], u[4], u[5], u[6], u[7], u[8])
                )

        package_count = db.execute('SELECT COUNT(*) FROM packages').fetchone()[0]
        if package_count == 0:
            # Seed packages from database.py
            initial_packages = [
                ("EXP001", "Ahmad Wijaya", "081234567890", "Siti Rahayu", "085678901234", "Jl. Merdeka No. 10, Jakarta Pusat", "Elektronik", 2.5, "15-02-2026", "D&L Super (Kilat)", "1-2 hari", 37500),
                ("EXP002", "Budi Santoso", "082345678901", "Ani Kusuma", "087654321098", "Jl. Sudirman No. 25, Bandung", "Pakaian/Tekstil", 1.2, "14-02-2026", "D&L Reguler", "2-5 hari", 12000),
                ("EXP003", "Dewi Lestari", "089012345678", "Rudi Hartono", "081234567890", "Jl. Gatot Subroto No. 50, Surabaya", "Dokumen", 0.5, "16-02-2026", "D&L Super (Kilat)", "1-2 hari", 7500)
            ]
            for p in initial_packages:
                db.execute(
                    "INSERT INTO packages (resi, sender, sender_phone, receiver, receiver_phone, destination_address, category, weight, shipping_date, shipping_type, estimation, fare) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    p
                )
        db.commit()

# Initialize Database on startup
init_db()

def calculate_fare(weight, shipping_type):
    tariff_per_kg = 10000
    if shipping_type == "D&L Reguler":
        tariff_per_kg = 10000
    elif shipping_type == "D&L Eco (Ekonomis)":
        tariff_per_kg = 7000
    elif shipping_type == "D&L Super (Kilat)":
        tariff_per_kg = 15000
    elif shipping_type == "D&L Cargo":
        tariff_per_kg = 8000
    return int(weight * tariff_per_kg)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    packages = db.execute('SELECT * FROM packages ORDER BY id DESC').fetchall()
    return render_template('index.html', packages=packages)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        email = request.form['email']
        gender = request.form.get('gender')
        age = request.form.get('age')
        occupation = request.form.get('occupation')
        city = request.form.get('city')
        phone = request.form.get('phone')
        
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, password, full_name, email, gender, age, occupation, city, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), full_name, email, gender, age, occupation, city, phone),
                )
                db.commit()
            except sqlite3.IntegrityError:
                error = f"User {username} is already registered."
            else:
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))

        flash(error, 'error')

    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username or password.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            return redirect(url_for('index'))

        flash(error, 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add_package', methods=('GET', 'POST'))
def add_package():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        resi = request.form['resi']
        sender = request.form['sender']
        sender_phone = request.form['sender_phone']
        receiver = request.form['receiver']
        receiver_phone = request.form['receiver_phone']
        destination_address = request.form['destination_address']
        category = request.form['category']
        weight = float(request.form['weight'])
        shipping_date = request.form['shipping_date']
        shipping_type = request.form['shipping_type']
        
        # Determine estimation
        estimation = "2-5 hari"
        if shipping_type == "D&L Eco (Ekonomis)":
            estimation = "3-7 hari"
        elif shipping_type == "D&L Super (Kilat)":
            estimation = "1-2 hari"
        elif shipping_type == "D&L Cargo":
            estimation = "Sesuai jadwal"
            
        fare = calculate_fare(weight, shipping_type)
        
        db = get_db()
        try:
            db.execute(
                "INSERT INTO packages (resi, sender, sender_phone, receiver, receiver_phone, destination_address, category, weight, shipping_date, shipping_type, estimation, fare) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (resi, sender, sender_phone, receiver, receiver_phone, destination_address, category, weight, shipping_date, shipping_type, estimation, fare)
            )
            db.commit()
            flash('Package added successfully!', 'success')
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            flash(f"Resi {resi} is already registered.", 'error')
            
    return render_template('add_package.html')

@app.route('/edit_package/<resi>', methods=('GET', 'POST'))
def edit_package(resi):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    package = db.execute('SELECT * FROM packages WHERE resi = ?', (resi,)).fetchone()
    
    if request.method == 'POST':
        sender = request.form['sender']
        sender_phone = request.form['sender_phone']
        receiver = request.form['receiver']
        receiver_phone = request.form['receiver_phone']
        destination_address = request.form['destination_address']
        category = request.form['category']
        weight = float(request.form['weight'])
        shipping_date = request.form['shipping_date']
        shipping_type = request.form['shipping_type']
        
        # Determine estimation (same logic as add)
        estimation = "2-5 hari"
        if shipping_type == "D&L Eco (Ekonomis)":
            estimation = "3-7 hari"
        elif shipping_type == "D&L Super (Kilat)":
            estimation = "1-2 hari"
        elif shipping_type == "D&L Cargo":
            estimation = "Sesuai jadwal"
            
        fare = calculate_fare(weight, shipping_type)
        
        db.execute(
            "UPDATE packages SET sender=?, sender_phone=?, receiver=?, receiver_phone=?, destination_address=?, category=?, weight=?, shipping_date=?, shipping_type=?, estimation=?, fare=? WHERE resi=?",
            (sender, sender_phone, receiver, receiver_phone, destination_address, category, weight, shipping_date, shipping_type, estimation, fare, resi)
        )
        db.commit()
        flash('Package updated successfully!', 'success')
        return redirect(url_for('index'))
        
    return render_template('edit_package.html', package=package)

@app.route('/delete_package/<resi>', methods=('POST',))
def delete_package(resi):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    db = get_db()
    db.execute('DELETE FROM packages WHERE resi = ?', (resi,))
    db.commit()
    flash('Package deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
