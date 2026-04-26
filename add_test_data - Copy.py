#!/usr/bin/env python3
"""
Test Data Generator for Medicine Scanner
Creates a test user and sample medicines for testing
Run this AFTER starting the app once to initialize the database
"""

import sqlite3
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

DATABASE = 'medicines.db'

def add_test_data():
    """Add test user and sample medicines to database"""
    
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()
    
    try:
        # Test user
        test_username = 'testuser'
        test_email = 'test@example.com'
        test_password = 'password123'
        
        cursor.execute(
            'INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
            (test_username, test_email, generate_password_hash(test_password))
        )
        db.commit()
        print(f"✅ Created test user:")
        print(f"   Username: {test_username}")
        print(f"   Email: {test_email}")
        print(f"   Password: {test_password}")
        
        # Get user ID
        cursor.execute('SELECT id FROM users WHERE username = ?', (test_username,))
        user_id = cursor.fetchone()[0]
        
        # Sample medicines
        today = datetime.now()
        medicines = [
            {
                'barcode': '5901234123457',
                'name': 'Paracetamol',
                'expiry': (today + timedelta(days=30)).strftime('%Y-%m-%d'),
                'use': 'For fever and pain relief'
            },
            {
                'barcode': '4006016721089',
                'name': 'Ibuprofen',
                'expiry': (today + timedelta(days=1)).strftime('%Y-%m-%d'),  # Expiring soon
                'use': 'For inflammation and pain'
            },
            {
                'barcode': '3574660156429',
                'name': 'Aspirin',
                'expiry': (today - timedelta(days=5)).strftime('%Y-%m-%d'),  # Already expired
                'use': 'For heart health and pain relief'
            },
            {
                'barcode': '5901234567890',
                'name': 'Vitamin C',
                'expiry': (today + timedelta(days=90)).strftime('%Y-%m-%d'),
                'use': 'Immune system support'
            },
            {
                'barcode': '5410076837125',
                'name': 'Cough Syrup',
                'expiry': (today + timedelta(days=2)).strftime('%Y-%m-%d'),  # Expiring in 2 days (alert)
                'use': 'For cough and cold relief'
            }
        ]
        
        # Insert medicines
        for medicine in medicines:
            cursor.execute(
                '''INSERT INTO medicines (user_id, barcode, name, expiry, use) 
                   VALUES (?, ?, ?, ?, ?)''',
                (user_id, medicine['barcode'], medicine['name'], 
                 medicine['expiry'], medicine['use'])
            )
        
        db.commit()
        print(f"\n✅ Added {len(medicines)} sample medicines:")
        for med in medicines:
            print(f"   • {med['name']} - Expires: {med['expiry']}")
        
        print("\n📝 Test Account Details:")
        print(f"   Username: {test_username}")
        print(f"   Password: {test_password}")
        print(f"   Email: {test_email} (for alerts)")
        
        print("\n🔍 Test Barcodes (for scanning):")
        for med in medicines:
            print(f"   {med['barcode']} - {med['name']}")
        
        print("\n✅ Test data added successfully!")
        print("   Start the app and login with the above credentials")
        
    except sqlite3.IntegrityError as e:
        print(f"⚠️  Test user already exists or duplicate data: {e}")
        print("   You can use existing test user to test the app")
    except Exception as e:
        print(f"❌ Error adding test data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    print("🧪 Medicine Scanner - Test Data Generator")
    print("=" * 50)
    print()
    
    # Check if database exists
    import os
    if not os.path.exists(DATABASE):
        print("❌ Database not found!")
        print("   Please start the app first with: python app.py")
        print("   This will create the database.")
        exit(1)
    
    print("📦 Adding test data to database...\n")
    add_test_data()
    
    print("\n" + "=" * 50)
    print("Ready to test! Start the app with: python app.py")
    print("=" * 50)
