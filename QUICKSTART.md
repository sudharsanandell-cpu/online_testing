# 🚀 Quick Start Guide - Smart Medicine Scanner

## ⚡ 5-Minute Setup

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure Email (Important!)
Open `app.py` and find lines 18-21:

```python
SENDER_EMAIL = "your-email@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "your-app-password"  # Your Gmail app password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

**Replace with your Gmail credentials:**
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click Security on the left
3. Enable "2-Step Verification"
4. Search for "App passwords"
5. Select Mail and your device
6. Copy the 16-character password
7. Paste it as `SENDER_PASSWORD`

### Step 3: Run the Application
```bash
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

### Step 4: Open in Browser
Go to `http://localhost:5000` and start using the app!

---

## 📋 What Each File Does

| File | Purpose |
|------|---------|
| `app.py` | Flask backend - handles all logic |
| `templates/login.html` | Login page |
| `templates/signup.html` | Registration page |
| `templates/index.html` | Main dashboard with scanner |
| `static/script.js` | JavaScript for frontend logic |
| `static/style.css` | Styling and layout |
| `medicines.db` | SQLite database (auto-created) |
| `requirements.txt` | Python packages needed |

---

## 🔐 Creating Your First Account

1. **Sign Up**: Click "Sign up here" on login page
2. **Enter Details**:
   - Username (any unique name)
   - Email (where you'll receive medicine alerts)
   - Password (min 6 characters)
3. **Login**: Use your credentials to login

---

## 📱 Using the Scanner

### Option 1: Camera Scan
1. Click "📷 Start Scanner"
2. Grant camera permission
3. Point at barcode
4. Scanner will auto-detect and lookup

### Option 2: Manual Entry
1. Click "Or enter barcode manually"
2. Type the barcode number
3. Click "Look Up"

### If Medicine Found ✅
- Shows: Name, Expiry Date, Usage
- Status indicator: Active / Expiring / Expired

### If Not Found ❌
- Enter: Medicine name, Expiry date, Usage
- Click "Save Medicine"

---

## 📧 Email Alert System

**Automatic:** System checks daily for medicines expiring in 2 days
**Example Alert:**
```
Subject: ⚠️ Medicine Expiry Alert: Paracetamol

Your medicine Paracetamol will expire on 2025-06-30
Please check your dashboard and replace it if needed.
```

---

## 🔧 Troubleshooting

### Camera Not Working?
- ✅ Grant camera permissions
- ✅ Use Chrome or Firefox
- ✅ Check if camera is used by another app

### Emails Not Sending?
- ✅ Verify Gmail app password (not regular password)
- ✅ Enable 2-Step Verification
- ✅ Check internet connection
- ✅ Look at app output for error messages

### App Won't Start?
- ✅ Install dependencies: `pip install -r requirements.txt`
- ✅ Check Python version (3.7+): `python --version`
- ✅ Make sure port 5000 is available
- ✅ Try running with: `python -u app.py`

### Can't Scan Barcode?
- ✅ Good lighting is important
- ✅ Keep barcode steady and centered
- ✅ Try manual entry instead
- ✅ Different barcode formats have different scan speeds

---

## 🛡️ Security Tips

1. **Change Secret Key**: Edit line 13 in `app.py`
   ```python
   app.secret_key = 'your-random-secure-key-here'
   ```

2. **Don't Share Credentials**:
   - Never commit `app.py` with real email password
   - Use environment variables in production

3. **In Production**:
   - Use HTTPS
   - Use a production server (Gunicorn)
   - Store secrets in environment variables
   - Enable CORS properly

---

## 📚 Example Barcodes to Test

Use these common product barcodes to test the scanner:
- **EAN-13**: 5901234123457 (Paracetamol)
- **UPC-A**: 012345678905

Or use any medicine from your home!

---

## 🎯 Features Summary

✅ User Registration & Login
✅ Real-time Barcode Scanning
✅ Medicine Database Management
✅ Expiry Date Tracking
✅ Automatic Email Alerts
✅ Responsive Design
✅ Clean UI
✅ SQLite Database

---

## 📞 Need Help?

1. Check the **README.md** for detailed documentation
2. Review code comments in `app.py`
3. Check browser console (F12) for JavaScript errors
4. Look at terminal output for Python errors

---

## 🎉 Happy Medicine Scanning!

Enjoy using your medicine scanner. Your health matters! 💊

For detailed API documentation and advanced features, see **README.md**
