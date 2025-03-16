#!/usr/bin/env python3
"""
Script to initialize the database with tables and initial data.
"""

import sqlite3
import os
import sys

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def execute_sql_script(conn, script_path):
    """
    Execute a SQL script.
    
    Args:
        conn: SQLite connection object
        script_path: Path to the SQL script
    """
    print(f"Executing SQL script: {script_path}")
    
    # Read the SQL script
    with open(script_path, 'r') as f:
        sql_script = f.read()
    
    # Split the script into individual statements
    statements = sql_script.split(';')
    
    # Execute each statement
    for statement in statements:
        if statement.strip():
            try:
                conn.execute(statement)
            except sqlite3.Error as e:
                print(f"Error executing SQL statement: {e}")
                print(f"Statement: {statement}")
    
    conn.commit()
    print(f"SQL script executed successfully: {script_path}")

def main():
    """
    Main function to run when the script is executed directly.
    """
    # Database file path
    db_path = os.path.join(os.path.dirname(__file__), '..', 'instance', 'development.db')
    
    # Ensure the instance directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Remove the database file if it exists
    if os.path.exists(db_path):
        print(f"Removing existing database: {db_path}")
        os.remove(db_path)
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    
    try:
        # Create the tables
        create_tables_script = os.path.join(os.path.dirname(__file__), 'create_tables.sql')
        execute_sql_script(conn, create_tables_script)
        
        # Insert initial data
        insert_data_script = os.path.join(os.path.dirname(__file__), 'insert_initial_data.sql')
        execute_sql_script(conn, insert_data_script)
        
        print("\nDatabase initialized successfully.")
        
        # Verify the data
        print("\nVerifying data...")
        
        # Verify admin user
        admin = conn.execute('''
            SELECT id, first_name, last_name, email, is_admin
            FROM users
            WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1'
        ''').fetchone()
        
        if admin:
            print(f"Admin user found: {admin[1]} {admin[2]} ({admin[3]}), is_admin: {admin[4]}")
        else:
            print("Admin user not found!")
        
        # Verify amenities
        amenities = conn.execute('''
            SELECT id, name
            FROM amenities
        ''').fetchall()
        
        print(f"Found {len(amenities)} amenities:")
        for amenity in amenities:
            print(f"- {amenity[1]} (ID: {amenity[0]})")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        # Close the connection
        conn.close()

if __name__ == "__main__":
    main()
