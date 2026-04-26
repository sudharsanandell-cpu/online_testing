# ✅ Setup & Launch Checklist

## 🔧 Pre-Launch Setup (Do This Once)

### 1. Install Python Packages
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify Flask installed: `python -c "import flask; print(flask.__version__)"`

### 2. Configure Email (CRITICAL!)
- [ ] Go to [myaccount.google.com](https://myaccount.google.com)
- [ ] Click "Security"
- [ ] Enable "2-Step Verification" (if not already)
- [ ] Search for "App passwords" at top of page
- [ ] Select "Mail" and your device type
- [ ] Copy the 16-character password
- [ ] Open `app.py`
- [ ] Go to line 18: `SENDER_EMAIL = "your-email@gmail.com"`
- [ ] Go to line 19: `SENDER_PASSWORD = "your-app-password"`
- [ ] Replace `your-email@gmail.com` with your Gmail (e.g., `john123@gmail.com`)
- [ ] Replace `your-app-password` with the 16-char password from Gmail
- [ ] Save the file

### 3. [Optional] Configure Secret Key
- [ ] Open `app.py`
- [ ] Go to line 13: `app.secret_key = 'your-secret-key-change-this'`
- [ ] Replace with a random string: `app.secret_key = 'sk_prod_abc123xyz456'`
- [ ] Save the file

### 4. Check Prerequisites
- [ ] Python 3.7+ installed: `python --version`
- [ ] Port 5000 is free (not used by other apps)
- [ ] Camera connected and working (if using barcode scanning)
- [ ] Internet connection (for Gmail SMTP)

---

## 🚀 First Time Launch

1. [ ] Open terminal/command prompt
2. [ ] Navigate to project folder: `cd medicine_scanner`
3. [ ] Run app: `python app.py`
4. [ ] See message: `Running on http://127.0.0.1:5000`
5. [ ] KEEP TERMINAL OPEN (don't close it)
6. [ ] Open browser to: `http://localhost:5000`

---

## 📝 Create Test Account

1. [ ] Click "Sign up here"
2. [ ] Enter username (e.g., `testuser`)
3. [ ] Enter your email (where you want alerts)
4. [ ] Enter password (min 6 chars, e.g., `password123`)
5. [ ] Submit form
6. [ ] See: "Signup successful! Please login."
7. [ ] Click link or go back to login page
8. [ ] Enter your username and password
9. [ ] See: Medicine Scanner Dashboard

---

## 📱 Testing the Scanner

### Test Option 1: Test Data (Easiest)
1. [ ] Stop app (Ctrl+C in terminal)
2. [ ] Run: `python add_test_data.py`
3. [ ] See test account created: `testuser` / `password123`
4. [ ] See sample medicines added
5. [ ] Restart app: `python app.py`
6. [ ] Login with testuser credentials
7. [ ] See medicines in "My Medicines" tab

### Test Option 2: Manual Barcode Entry
1. [ ] Use sample barcodes:
   - `5901234123457` (Paracetamol)
   - `4006016721089` (Ibuprofen)
2. [ ] On dashboard, scroll down to manual entry
3. [ ] Copy barcode above
4. [ ] Paste into input field
5. [ ] Click "Look Up"
6. [ ] See form to add medicine details
7. [ ] Fill in name, expiry, usage
8. [ ] Click "Save Medicine"
9. [ ] See success message and medicine details

### Test Option 3: Real Barcode Scanning
1. [ ] Have a medicine box with barcode
2. [ ] Click "📷 Start Scanner"
3. [ ] Grant camera permission if asked
4. [ ] Hold barcode in front of camera
5. [ ] Keep steady for 2-3 seconds
6. [ ] See: barcode detected and auto-searched
7. [ ] Either shows medicine or form to add new one

---

## 🧪 Test Email Alerts

### Manual Test:
1. [ ] Add medicine with expiry in 1-2 days from now
2. [ ] Check app console for: "Email sent to..."
3. [ ] Check your email inbox for alert

### Auto Test:
1. [ ] Set expiry to exactly 1 day from now
2. [ ] Wait 24 hours OR modify app to check more frequently
3. [ ] Email should arrive to your registered email

---

## 📋 Verify All Features Work

### Authentication
- [ ] Signup creates new account
- [ ] Login with correct password works
- [ ] Login with wrong password fails
- [ ] Logout returns to login page
- [ ] Cannot access dashboard without login

### Barcode Scanning
- [ ] Camera starts when "Start Scanner" clicked
- [ ] Barcode detected and auto-lookup works
- [ ] Manual entry works
- [ ] If barcode not found, form appears

### Medicine Management
- [ ] Can add new medicine
- [ ] Medicine appears in "My Medicines" tab
- [ ] Can view all medicines in grid
- [ ] Can delete medicine
- [ ] Medicine list updates correctly

### Status Indicators
- [ ] Active medicines: Green ✓
- [ ] Expiring in 2 days: Orange ⚡
- [ ] Expired medicines: Red ⚠️

### Email Alerts
- [ ] Medicines set to expire in 1-2 days trigger alerts
- [ ] Emails sent to registered email
- [ ] Email contains medicine name and expiry date

---

## ⚠️ Troubleshooting

### App Won't Start
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Check Python version: `python --version` (need 3.7+)
- [ ] Try different port: Edit `app.run()` in app.py
- [ ] Check for error messages in terminal

### Camera Not Working
- [ ] Grant camera permissions in browser
- [ ] Refresh page (F5)
- [ ] Use Chrome or Firefox (better support)
- [ ] Check if camera is used by another app
- [ ] Try manual barcode entry instead

### Email Not Working
- [ ] Verify email didn't auto-correct in app.py
- [ ] Use app password, NOT regular Gmail password
- [ ] Check 2-Step Verification is enabled
- [ ] Look for errors in terminal output
- [ ] Test internet connection

### Database Errors
- [ ] Delete `medicines.db` file
- [ ] Restart app (it will recreate database)
- [ ] Should see: "Database initialized successfully"

---

## 📊 File Checklist

Verify all files are present:
- [ ] `app.py` - Flask application
- [ ] `requirements.txt` - Dependencies
- [ ] `README.md` - Full documentation
- [ ] `QUICKSTART.md` - Quick setup guide
- [ ] `SUMMARY.md` - Project summary
- [ ] `CHECKLIST.md` - This file
- [ ] `add_test_data.py` - Test data script
- [ ] `templates/login.html` - Login page
- [ ] `templates/signup.html` - Signup page
- [ ] `templates/index.html` - Dashboard
- [ ] `static/script.js` - Frontend logic
- [ ] `static/style.css` - Styling

---

## 🎯 Quick Command Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Start the application
python app.py

# Add test data (after first app start)
python add_test_data.py

# Check Python version
python --version

# Stop the app
Ctrl+C (in terminal)

# Open in browser
http://localhost:5000
```

---

## 💡 Pro Tips

1. **Keep terminal open** while using the app (shows logs)
2. **Use test data** first to verify everything works
3. **Check terminal** for any error messages
4. **Clear browser cache** if UI looks strange (Ctrl+Shift+Delete)
5. **Use Chrome/Firefox** for best barcode scanning
6. **Good lighting** helps barcode detection
7. **Keep barcode steady** when scanning
8. **Check spam folder** for alert emails

---

## ✅ All Set!

If you've completed this checklist:
1. ✅ App is running
2. ✅ Can login
3. ✅ Can scan barcodes
4. ✅ Can manage medicines
5. ✅ Will receive email alerts

## 🎉 You're Ready to Use Smart Medicine Scanner!

For detailed documentation, see **README.md**
For quick reference, see **QUICKSTART.md**

**Stay healthy! 💊**
