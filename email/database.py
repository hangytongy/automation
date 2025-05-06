import sqlite3
import os

def init_db(db_name):

    # Check if database already exists
    if not os.path.exists(db_name):
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Create the table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            name TEXT,
            total_amount REAL,
            start_date TEXT,
            payment_type TEXT,
            payment_address TEXT,
            invoice_no INTEGER
        )
        """)

        conn.commit()
        conn.close()
        print("Database and table created.")
    else:
        print("Database already exists. Skipping creation.")


def insert_invoice(db_path,name,total_amount,start_date,payment_type,payment_address,invoice_no):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO invoices (name,total_amount,start_date,payment_type,payment_address,invoice_no)
        VALUES (?, ?, ?, ?, ?, ?)
    """, 
    (name,total_amount,start_date,payment_type,payment_address,invoice_no)
    )

    conn.commit()
    conn.close()

    print(f"database updated : Add INV-{name}-{invoice_no}")


def delete_invoice(db_path, name, invoice_no):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM invoices
        WHERE name = ? AND invoice_no = ?    
        """,
        (name,invoice_no)
        )
    
    conn.commit()
    conn.close()

    print(f"database updated : Delete INV-{name}-{invoice_no}")




