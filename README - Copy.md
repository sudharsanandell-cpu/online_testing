# 💊 Smart Medicine Barcode Scanner Web Application

A complete web application for scanning medicine barcodes, storing medicine details in a SQLite database, and automatically sending email alerts for medicines expiring within 2 days.

## Features

✅ **User Authentication**
- Signup system with email validation
- Secure login with password hashing
- Session management

✅ **Barcode Scanning**
- Real-time barcode scanning using QuaggaJS
- Support for multiple barcode formats
- Manual barcode entry option

✅ **Medicine Management**
- Add new medicines with barcode, name, expiry date, and usage
- View all saved medicines in a organized grid
- Delete medicines
- Track medicine expiry status

✅ **Smart Expiry Alerts**
- Automatic email notifications for medicines expiring within 2 days
- Daily background check for upcoming expirations
- Customizable alert messages

✅ **User-Friendly UI**
- Responsive design for desktop and mobile
- Clean, modern interface
- Real-time status indicators (Active, Expiring Soon, Expired)

## System Architecture

```
medicine_scanner/
├── app.py                 # Flask backend with all routes
├── requirements.txt       # Python dependencies
├── medicines.db          # SQLite database (auto-created)
├── templates/
│   ├── login.html        # Login page
│   ├── signup.html       # Registration page
│   └── index.html        # Main dashboard
└── static/
    ├── script.js         # Frontend logic
    └── style.css         # Styling
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Medicines Table
```sql
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
```

## Installation & Setup

### 1. Prerequisites
- Python 3.7 or higher
- pip (Python package manager)
- A Gmail account (for email alerts)

### 2. Clone/Setup the Project
```bash
cd medicine_scanner
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Email (IMPORTANT!)

Edit `app.py` and update the email configuration on lines 18-21:

```python
SENDER_EMAIL = "your-email@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "your-app-password"  # Your Gmail app password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

**How to Get Gmail App Password:**
1. Go to [Google Account](https://myaccount.google.com/)
2. Click "Security" in the left sidebar
3. Enable "2-Step Verification" if not already enabled
4. Search for "App passwords" at the top
5. Select "Mail" and "Windows Computer" (or your device)
6. Copy the generated 16-character password
7. Use this as your `SENDER_PASSWORD` in app.py

### 5. Run the Application
```bash
python app.py
```

The app will start at `http://localhost:5000`

## Usage Guide

### 1. Create an Account
- Click "Sign up here" on the login page
- Enter username, email, and password
- Account will be created in the SQLite database

### 2. Login
- Enter your credentials
- You'll be redirected to the main scanner dashboard

### 3. Scan Medicines
- Click "📷 Start Scanner" to open camera
- Point camera at barcode
- Or enter barcode manually and click "Look Up"

### 4. Add New Medicine
- If barcode not found, enter:
  - Medicine name (e.g., "Paracetamol")
  - Expiry date (using date picker)
  - Usage/purpose (e.g., "For fever and pain relief")
- Click "Save Medicine"

### 5. View All Medicines
- Click on "📋 My Medicines" tab
- See all your saved medicines with status indicators
- Delete medicines you no longer need

### 6. Email Alerts
- System automatically checks daily at midnight
- Medicines expiring within 2 days will trigger email alerts
- Emails are sent to your registered email address

## API Endpoints

| Route | Method | Purpose |
|-------|--------|---------|
| `/login` | GET/POST | User login |
| `/signup` | GET/POST | User registration |
| `/logout` | GET | Logout user |
| `/` | GET | Main dashboard (requires auth) |
| `/scan` | POST | Lookup barcode |
| `/save` | POST | Save new medicine |
| `/get-medicines` | GET | Get all medicines for user |
| `/delete-medicine/<id>` | DELETE | Delete a medicine |

## API Request/Response Examples

### Scan Barcode
```bash
POST /scan
Content-Type: application/json

{
    "barcode": "5901234123457"
}

Response:
{
    "status": "found",
    "id": 1,
    "barcode": "5901234123457",
    "name": "Paracetamol",
    "expiry": "2025-06-30",
    "use": "For fever and pain relief"
}
```

### Save Medicine
```bash
POST /save
Content-Type: application/json

{
    "barcode": "5901234123457",
    "name": "Paracetamol",
    "expiry": "2025-06-30",
    "use": "For fever and pain relief"
}

Response:
{
    "status": "success",
    "message": "Medicine saved successfully",
    "id": 1
}
```

## Email Alert Format

When a medicine is expiring within 2 days, users receive an email like:

```
Subject: ⚠️ Medicine Expiry Alert: Paracetamol

Body:
Hi username,

Your medicine Paracetamol will expire on 2025-06-30

Please check your medicine dashboard and replace it if needed.

Best regards,
Smart Medicine Scanner Team
```

## Troubleshooting

### Camera not working
- Grant camera permissions to the browser
- Use Chrome or Firefox (better compatibility)
- Check if camera is being used by another app

### Emails not being sent
- Verify Gmail credentials and app password
- Check "Less secure app access" settings if using regular password
- Ensure your Flask app has internet connection
- Check logs for error messages

### JavaScript errors
- Clear browser cache (Ctrl+Shift+Delete)
- Ensure QuaggaJS is loaded from CDN
- Check browser console (F12) for specific errors

### Database locked
- Close all instances of the app
- Delete `.db-journal` file if present
- Restart the application

## Security Notes

1. **Change the secret key** in app.py line 13:
   ```python
   app.secret_key = 'change-this-to-random-string'
   ```

2. **Never commit sensitive data**:
   - Email credentials
   - Database files with actual data
   - Secret keys

3. **Use environment variables** in production:
   ```python
   import os
   SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
   SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
   ```

## Performance Optimization

For production deployment:
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Enable database connection pooling
3. Implement caching for frequently accessed data
4. Use HTTPS for secure data transmission
5. Scale the expiry checker as a separate service

## Future Enhancements

- [ ] Mobile app using React Native
- [ ] Cloud storage integration
- [ ] Prescription management
- [ ] Multiple family member accounts
- [ ] Medicine interaction checker
- [ ] Pharmacy integration for quick refills
- [ ] QR code generation for tracking
- [ ] SMS alerts in addition to email
- [ ] PDF reports of medicines

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Check browser console for errors (F12)

---

**Version:** 1.0.0  
**Last Updated:** 2024  
**Status:** Production Ready ✅
```

Replace `YOUR_PROJECT_ID` with your actual Firebase project ID.

### 4. Setup Firebase Database Rules

In Firebase Console → Realtime Database → Rules, paste:

```json
{
  "rules": {
    "medicines": {
      ".read": true,
      ".write": true
    }
  }
}
```

⚠️ **Note**: This allows public read/write. For production, implement proper authentication.

### 5. Run the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Firebase Database Structure

Medicines are stored in the following structure:

```
medicines/
├── 5901234123457/
│   ├── name: "Aspirin 500mg"
│   ├── expiry: "2025-12-31"
│   └── use: "Pain relief and fever reduction"
├── 5012345678901/
│   ├── name: "Ibuprofen 200mg"
│   ├── expiry: "2026-06-15"
│   └── use: "Anti-inflammatory and pain relief"
```

## API Endpoints

### POST /scan
Scan a barcode and get medicine details.

**Request:**
```json
{
    "barcode": "5901234123457"
}
```

**Response (Found):**
```json
{
    "status": "found",
    "barcode": "5901234123457",
    "name": "Aspirin 500mg",
    "expiry": "2025-12-31",
    "use": "Pain relief"
}
```

**Response (Not Found):**
```json
{
    "status": "not_found",
    "barcode": "5901234123457"
}
```

### POST /save
Save a new medicine to the database.

**Request:**
```json
{
    "barcode": "5901234123457",
    "name": "Aspirin 500mg",
    "expiry": "2025-12-31",
    "use": "Pain relief and fever reduction"
}
```

**Response:**
```json
{
    "status": "success",
    "message": "Medicine saved successfully"
}
```

## Usage

1. Click **"📷 Start Scanning"** to open the camera
2. Point the camera at a barcode
3. The app will automatically scan and look up the medicine
4. If found → see medicine details
5. If not found → enter the medicine information and save

Alternatively, manually enter the barcode number and click "Look Up".

## Technologies Used

- **Backend**: Flask (Python)
- **Database**: Firebase Realtime Database
- **Frontend**: HTML5, CSS3, JavaScript
- **Barcode Scanner**: QuaggaJS
- **Icons**: Unicode emojis

## Browser Requirements

- Must support **WebRTC** and **getUserMedia API**
- Works on: Chrome, Firefox, Edge, Safari (iOS 14.5+)
- Requires **HTTPS** for camera access (except localhost)

## Troubleshooting

### Camera not working
- Ensure you grant camera permissions
- Use HTTPS in production
- Check if another app is using the camera

### Firebase connection issues
- Verify `serviceAccountKey.json` exists and is valid
- Check database URL in `app.py`
- Ensure Firebase credentials have Realtime Database access

### Barcode not scanning
- Ensure barcode is in good lighting
- Try different barcode formats (CODE128, EAN13, etc.)
- Check browser console for errors

## Sample Test Barcodes

Some standard product barcodes to test:
- `5901234123457` - Aspirin
- `5012345678901` - Ibuprofen
- `1234567890123` - Custom test

## Security Notes

⚠️ **Important**: The current setup allows public read/write to Firebase. For production:

1. Implement proper authentication
2. Use Firebase Security Rules to restrict access
3. Store API keys securely
4. Validate all inputs on the backend
5. Rate limit API endpoints

## License

MIT License - Feel free to modify and use this project.

## Support

For issues with:
- **QuaggaJS**: Check [QuaggaJS Documentation](https://serratus.github.io/quaggaJS/)
- **Firebase**: Check [Firebase Docs](https://firebase.google.com/docs)
- **Flask**: Check [Flask Documentation](https://flask.palletsprojects.com/)
