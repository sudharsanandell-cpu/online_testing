from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
import sqlite3
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from PIL import Image
import base64
import tempfile

# Optional: Try to import pyzbar for barcode image scanning
try:
    from pyzbar.pyzbar import decode
    PYZBAR_AVAILABLE = True
except (ImportError, FileNotFoundError, OSError):
    PYZBAR_AVAILABLE = False
    decode = None

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

DATABASE = 'medicines.db'

# SQLite options: allow more concurrent reads/writes and avoid transient locks.
DB_LOCK = threading.Lock()

# ==================== EMAIL CONFIGURATION ====================
SENDER_EMAIL = "your-email@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "your-app-password"  # Your Gmail app password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# ==================== DATABASE SETUP ====================
def get_db():
    db = sqlite3.connect(DATABASE, timeout=30, check_same_thread=False)
    db.row_factory = sqlite3.Row
    db.execute('PRAGMA journal_mode=WAL')
    db.execute('PRAGMA synchronous=NORMAL')
    return db

def init_db():
    """Create database tables if they don't exist"""
    if not os.path.exists(DATABASE):
        db = sqlite3.connect(DATABASE)
        cursor = db.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create medicines table
        cursor.execute('''
            CREATE TABLE medicines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                barcode TEXT NOT NULL,
                name TEXT NOT NULL,
                expiry TEXT NOT NULL,
                use TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, barcode)
            )
        ''')
        
        db.commit()
        db.close()
        print("Database initialized successfully")

# ==================== EMAIL FUNCTIONS ====================
def send_email(recipient_email, subject, body):
    """Send email alert"""
    try:
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = recipient_email
        message["Subject"] = subject
        
        message.attach(MIMEText(body, "html"))
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)
        
        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_and_send_expiry_alerts():
    """Check for medicines expiring soon and send alerts"""
    db = get_db()
    cursor = db.cursor()
    
    # Get all medicines expiring within 2 days
    alert_date = (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT m.id, m.name, m.expiry, u.email, u.username 
        FROM medicines m
        JOIN users u ON m.user_id = u.id
        WHERE m.expiry >= ? AND m.expiry <= ?
    ''', (today, alert_date))
    
    records = cursor.fetchall()
    db.close()
    
    for record in records:
        subject = f"⚠️ Medicine Expiry Alert: {record['name']}"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Medicine Expiry Alert</h2>
            <p>Hi {record['username']},</p>
            <p><strong>Your medicine {record['name']} will expire on {record['expiry']}</strong></p>
            <p>Please check your medicine dashboard and replace it if needed.</p>
            <p>Best regards,<br>Smart Medicine Scanner Team</p>
        </body>
        </html>
        """
        send_email(record['email'], subject, body)

# ==================== AUTHENTICATION ROUTES ====================
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not email or not password:
            return jsonify({"status": "error", "message": "All fields required"}), 400
        
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                (username, email, generate_password_hash(password))
            )
            db.commit()
            db.close()
            return jsonify({"status": "success", "message": "Signup successful! Please login."})
        except sqlite3.IntegrityError:
            return jsonify({"status": "error", "message": "Username or email already exists"}), 400
    
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({"status": "error", "message": "Username and password required"}), 400
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        db.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return jsonify({"status": "success", "message": "Login successful"})
        else:
            return jsonify({"status": "error", "message": "Invalid username or password"}), 401
    
    if 'user_id' in session:
        return redirect(url_for('index'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==================== MAIN ROUTES ====================
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))

@app.route('/scan', methods=['POST'])
def scan():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    try:
        data = request.json
        barcode = data.get('barcode', '').strip()
        user_id = session['user_id']
        
        if not barcode:
            return jsonify({"status": "error", "message": "Barcode required"}), 400
        
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT * FROM medicines WHERE user_id = ? AND barcode = ?',
            (user_id, barcode)
        )
        medicine = cursor.fetchone()
        db.close()
        
        if medicine:
            return jsonify({
                "status": "found",
                "id": medicine['id'],
                "barcode": medicine['barcode'],
                "name": medicine['name'],
                "expiry": medicine['expiry'],
                "use": medicine['use']
            })
        else:
            return jsonify({"status": "not_found", "barcode": barcode})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/save', methods=['POST'])
def save():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    try:
        data = request.json
        user_id = session['user_id']
        barcode = data.get('barcode', '').strip()
        name = data.get('name', '').strip()
        expiry = data.get('expiry', '').strip()
        use = data.get('use', '').strip()
        
        if not all([barcode, name, expiry, use]):
            return jsonify({"status": "error", "message": "All fields required"}), 400
        
        with DB_LOCK:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                '''INSERT INTO medicines (user_id, barcode, name, expiry, use) 
                   VALUES (?, ?, ?, ?, ?)''',
                (user_id, barcode, name, expiry, use)
            )
            db.commit()
            medicine_id = cursor.lastrowid
        db.close()
        
        return jsonify({
            "status": "success",
            "message": "Medicine saved successfully",
            "id": medicine_id,
            "barcode": barcode,
            "name": name,
            "expiry": expiry,
            "use": use
        })
    
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "This barcode already exists for your account"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/get-medicines', methods=['GET'])
def get_medicines():
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            'SELECT id, barcode, name, expiry, use FROM medicines WHERE user_id = ? ORDER BY created_at DESC',
            (session['user_id'],)
        )
        medicines = [dict(row) for row in cursor.fetchall()]
        db.close()
        return jsonify({"status": "success", "medicines": medicines})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete-medicine/<int:medicine_id>', methods=['DELETE'])
def delete_medicine(medicine_id):
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    try:
        with DB_LOCK:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                'DELETE FROM medicines WHERE id = ? AND user_id = ?',
                (medicine_id, session['user_id'])
            )
            db.commit()
        db.close()
        return jsonify({"status": "success", "message": "Medicine deleted"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==================== BARCODE GENERATOR ====================
@app.route('/generate-barcode', methods=['GET', 'POST'])
def generate_barcode():
    """Generate and return a barcode image as PNG"""
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    try:
        # Handle both JSON and form data
        if request.method == 'POST':
            if request.is_json:
                data = request.json
            else:
                data = request.form
        else:
            return jsonify({"status": "error", "message": "Please use the barcode generator in the app"}), 400
        
        barcode_num = data.get('barcode', '').strip()
        medicine_name = data.get('medicine_name', 'Medicine').strip()
        
        if not barcode_num:
            return jsonify({"status": "error", "message": "Barcode number required"}), 400
        
        # Validate barcode is numeric
        if not barcode_num.isdigit():
            return jsonify({"status": "error", "message": "Barcode must contain only digits"}), 400
        
        # Pad to 12 digits if needed
        if len(barcode_num) < 12:
            barcode_num = barcode_num.zfill(12)
        elif len(barcode_num) > 13:
            return jsonify({"status": "error", "message": "Barcode must be 12-13 digits maximum"}), 400
        
        # Create EAN-13 barcode with high DPI
        ean = barcode.get('ean13', barcode_num, writer=ImageWriter())
        
        # Generate image in memory with high quality
        image_buffer = BytesIO()
        ean.write(image_buffer, options={
            'write_text': True,
            'text_distance': 5,
            'dpi': 300
        })
        image_buffer.seek(0)
        
        return send_file(
            image_buffer,
            mimetype='image/png',
            as_attachment=True,
            download_name=f'barcode_{barcode_num}_{medicine_name}.png'
        )
    
    except Exception as e:
        print(f"Generate barcode error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/generate-barcode-display', methods=['POST'])
def generate_barcode_display():
    """Generate barcode and return as base64 for display"""
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    try:
        data = request.json
        barcode_num = data.get('barcode', '').strip()
        
        if not barcode_num:
            return jsonify({"status": "error", "message": "Barcode number required"}), 400
        
        # Validate barcode is numeric
        if not barcode_num.isdigit():
            return jsonify({"status": "error", "message": "Barcode must contain only digits"}), 400
        
        # EAN-13 requires 12 or 13 digits
        if len(barcode_num) > 13:
            return jsonify({"status": "error", "message": "Barcode must be 12-13 digits maximum"}), 400
        
        # Pad to 12 digits if needed
        if len(barcode_num) < 12:
            barcode_num = barcode_num.zfill(12)
        
        # Create EAN-13 barcode with higher DPI for better scanning
        from barcode.writer import ImageWriter
        
        # Create writer with custom settings for better quality
        writer = ImageWriter()
        ean = barcode.get('ean13', barcode_num, writer=writer)
        
        # Generate image in memory with large size
        image_buffer = BytesIO()
        ean.write(image_buffer, options={
            'write_text': True,
            'text_distance': 5,
            'dpi': 300  # High DPI for better quality
        })
        image_buffer.seek(0)
        
        # Convert to base64
        import base64
        image_base64 = base64.b64encode(image_buffer.getvalue()).decode()
        
        return jsonify({
            "status": "success",
            "image": f"data:image/png;base64,{image_base64}",
            "barcode": barcode_num,
            "message": "Barcode generated successfully. Print this or enlarge on screen to scan."
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# ==================== BARCODE IMAGE SCANNER ====================
@app.route('/scan-image', methods=['POST'])
def scan_image():
    """Decode barcode from uploaded image file"""
    if 'user_id' not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401
    
    # Check if pyzbar is available
    if not PYZBAR_AVAILABLE:
        return jsonify({
            "status": "error",
            "message": "Barcode image scanning is not available on this system. Please use manual entry or camera scanner instead."
        }), 503
    
    try:
        # Check if file was uploaded
        if 'barcode_image' not in request.files:
            return jsonify({"status": "error", "message": "No image file provided"}), 400
        
        file = request.files['barcode_image']
        
        if file.filename == '':
            return jsonify({"status": "error", "message": "No file selected"}), 400
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({"status": "error", "message": "Invalid file type. Allowed: PNG, JPG, GIF, BMP, WEBP"}), 400
        
        try:
            # Open image from file
            img = Image.open(file.stream)
            
            # Decode barcodes from image
            decoded_objects = decode(img)
            
            if not decoded_objects:
                return jsonify({
                    "status": "not_found",
                    "message": "No barcode detected in image. Try another image or use manual entry."
                })
            
            # Get the first barcode found
            barcode_obj = decoded_objects[0]
            barcode_data = barcode_obj.data.decode('utf-8')
            barcode_type = barcode_obj.type
            
            print(f"Barcode decoded: {barcode_data} (Type: {barcode_type})")
            
            return jsonify({
                "status": "success",
                "barcode": barcode_data,
                "type": barcode_type,
                "message": f"Barcode detected: {barcode_type}"
            })
        
        except Exception as e:
            print(f"Image processing error: {e}")
            return jsonify({"status": "error", "message": f"Error processing image: {str(e)}"}), 400
    
    except Exception as e:
        print(f"Scan image error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
def start_expiry_checker():
    """Run expiry checker in background (every 24 hours)"""
    import time
    while True:
        try:
            check_and_send_expiry_alerts()
        except Exception as e:
            print(f"Error in expiry checker: {e}")
        time.sleep(86400)  # Check every 24 hours

# ==================== APP INITIALIZATION ====================
if __name__ == '__main__':
    init_db()
    
    # Start expiry checker in background thread
    checker_thread = threading.Thread(target=start_expiry_checker, daemon=True)
    checker_thread.start()
    
    app.run(debug=True) 