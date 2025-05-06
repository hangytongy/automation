import sqlite3
from datetime import datetime, timedelta
from post_telegram import send_message_telegram
import os

def check_outstanding_invoices(db_path: str) -> None:
    """
    Check for unpaid invoices and send reminders if needed.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query for all invoices
    cursor.execute("""
        SELECT name, total_amount, start_date, invoice_no
        FROM invoices
    """)
    
    unpaid_invoices = cursor.fetchall()
    
    for invoice in unpaid_invoices:
        name, total_amount, start_date, invoice_no = invoice

        # Calculate days overdue
        start_date_obj = datetime.strptime(start_date, "%d %b'%y")
        days_overdue = (datetime.now() - start_date_obj).days
        
        # Check if we should send a reminder based on invoice date
        if should_send_reminder(days_overdue):
            # Send reminder via telegram
            message = f"INV-{name}-{invoice_no} from {start_date} has not been paid for {days_overdue} days"
            send_message_telegram(message)

    conn.close()
    

def should_send_reminder(days_since_invoice : int) -> bool:
    """
    Determine if a reminder should be sent based on invoice date.
    Returns True if enough time has passed since invoice was created.
    """
    
    # Send reminder every 7 days
    return days_since_invoice % 7 == 0 and days_since_invoice > 0


db_name = "invoices_pending.db"
if os.path.exists(db_name):
    check_outstanding_invoices(db_name)
else:
    print(f"Database {db_name} not available")