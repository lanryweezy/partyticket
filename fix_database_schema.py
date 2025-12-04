"""Migration script to fix database schema issues."""

import sqlite3
import os

def fix_database_schema():
    """Fix database schema issues."""
    # Connect to the database
    db_path = os.path.join('instance', 'site.db')
    if not os.path.exists(db_path):
        print("Database file not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]
    print(f"Existing tables: {tables}")
    
    # Add missing columns to event table if they don't exist
    try:
        cursor.execute("ALTER TABLE event ADD COLUMN category VARCHAR(50) DEFAULT 'general'")
        print("Added category column to event table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Category column already exists in event table")
        else:
            print(f"Error adding category column: {e}")
    
    try:
        cursor.execute("ALTER TABLE event ADD COLUMN invitation_fee FLOAT DEFAULT 0.0")
        print("Added invitation_fee column to event table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("invitation_fee column already exists in event table")
        else:
            print(f"Error adding invitation_fee column: {e}")
    
    try:
        cursor.execute("ALTER TABLE event ADD COLUMN date_created DATETIME DEFAULT CURRENT_TIMESTAMP")
        print("Added date_created column to event table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("date_created column already exists in event table")
        else:
            print(f"Error adding date_created column: {e}")
    
    # Add missing columns to invitation table if they don't exist
    try:
        cursor.execute("ALTER TABLE invitation ADD COLUMN invitation_data TEXT")
        print("Added invitation_data column to invitation table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("invitation_data column already exists in invitation table")
        else:
            print(f"Error adding invitation_data column: {e}")
    
    try:
        cursor.execute("ALTER TABLE invitation ADD COLUMN amount_paid FLOAT DEFAULT 0.0")
        print("Added amount_paid column to invitation table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("amount_paid column already exists in invitation table")
        else:
            print(f"Error adding amount_paid column: {e}")
    
    try:
        cursor.execute("ALTER TABLE invitation ADD COLUMN attendee_count INTEGER DEFAULT 0")
        print("Added attendee_count column to invitation table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("attendee_count column already exists in invitation table")
        else:
            print(f"Error adding attendee_count column: {e}")
    
    # Add missing columns to ticket table if they don't exist
    try:
        cursor.execute("ALTER TABLE ticket ADD COLUMN ticket_data TEXT")
        print("Added ticket_data column to ticket table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ticket_data column already exists in ticket table")
        else:
            print(f"Error adding ticket_data column: {e}")
    
    try:
        cursor.execute("ALTER TABLE ticket ADD COLUMN amount_paid FLOAT DEFAULT 0.0")
        print("Added amount_paid column to ticket table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("amount_paid column already exists in ticket table")
        else:
            print(f"Error adding amount_paid column: {e}")
    
    try:
        cursor.execute("ALTER TABLE ticket ADD COLUMN date_purchased DATETIME DEFAULT CURRENT_TIMESTAMP")
        print("Added date_purchased column to ticket table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("date_purchased column already exists in ticket table")
        else:
            print(f"Error adding date_purchased column: {e}")
    
    # Add missing columns to user table if they don't exist
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN email VARCHAR(150)")
        print("Added email column to user table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("email column already exists in user table")
        else:
            print(f"Error adding email column: {e}")
    
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN phone VARCHAR(20)")
        print("Added phone column to user table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("phone column already exists in user table")
        else:
            print(f"Error adding phone column: {e}")
    
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN is_student BOOLEAN DEFAULT 0")
        print("Added is_student column to user table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("is_student column already exists in user table")
        else:
            print(f"Error adding is_student column: {e}")
    
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN is_verified_student BOOLEAN DEFAULT 0")
        print("Added is_verified_student column to user table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("is_verified_student column already exists in user table")
        else:
            print(f"Error adding is_verified_student column: {e}")
    
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN school VARCHAR(150)")
        print("Added school column to user table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("school column already exists in user table")
        else:
            print(f"Error adding school column: {e}")
    
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN student_id VARCHAR(50)")
        print("Added student_id column to user table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("student_id column already exists in user table")
        else:
            print(f"Error adding student_id column: {e}")
    
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN earnings FLOAT DEFAULT 0.0")
        print("Added earnings column to user table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("earnings column already exists in user table")
        else:
            print(f"Error adding earnings column: {e}")
    
    try:
        cursor.execute("ALTER TABLE user ADD COLUMN date_registered DATETIME DEFAULT CURRENT_TIMESTAMP")
        print("Added date_registered column to user table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("date_registered column already exists in user table")
        else:
            print(f"Error adding date_registered column: {e}")
    
    # Add missing columns to blog_post table if they don't exist
    try:
        cursor.execute("ALTER TABLE blog_post ADD COLUMN slug VARCHAR(200)")
        print("Added slug column to blog_post table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("slug column already exists in blog_post table")
        else:
            print(f"Error adding slug column: {e}")
    
    try:
        cursor.execute("ALTER TABLE blog_post ADD COLUMN published BOOLEAN DEFAULT 0")
        print("Added published column to blog_post table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("published column already exists in blog_post table")
        else:
            print(f"Error adding published column: {e}")
    
    try:
        cursor.execute("ALTER TABLE blog_post ADD COLUMN views INTEGER DEFAULT 0")
        print("Added views column to blog_post table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("views column already exists in blog_post table")
        else:
            print(f"Error adding views column: {e}")
    
    try:
        cursor.execute("ALTER TABLE blog_post ADD COLUMN date_posted DATETIME DEFAULT CURRENT_TIMESTAMP")
        print("Added date_posted column to blog_post table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("date_posted column already exists in blog_post table")
        else:
            print(f"Error adding date_posted column: {e}")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database schema fixed successfully!")

if __name__ == "__main__":
    fix_database_schema()