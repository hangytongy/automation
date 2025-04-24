import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from post_telegram import send_message_telegram

load_dotenv()


def send_email(project,end_date,invoice_path):

    name = project['project']

    if project["mail_list"]:
    
        payment_type = project['payment_type']
        payment_address = project['payment_address']
        amounts = project['amount']
        
        total = 0
        for amount in amounts:
            total += amount
        
        #sign off
        signature = f"Regards, \nHanrong (Mr.) \nAdmin \nMetafrontier Ltd"
        
        # Settings
        gmail_user = os.getenv("gmail_user")
        gmail_app_password = os.getenv("gmail_app_password")
        to_email = os.getenv("to_email")

        # Generate dynamic content
        month = datetime.now().strftime("%B %Y")
        subject = f"Community Management Services for {name}"
        body = f"Hi team,\n\nSending over the invoice for {name}'s Community Management Services. Attached is the invoice for the period ending {end_date}.\n\nPlease pay {total:,} to the following {payment_type} address: \n{payment_address} \n\n{signature}" 

        
        cc_email_str = os.getenv("cc_email") 
        cc_email_list = [email.strip() for email in cc_email_str.split(",")] if cc_email_str else []

        # Create message
        msg = EmailMessage()
        msg['From'] = gmail_user
        msg['To'] = ", ".join(project["mail_list"])
        msg["Cc"] = ", ".join(cc_email_list) 
        msg['Subject'] = subject
        msg.set_content(body)

        # Attach invoice
        try:
            with open(invoice_path, "rb") as f:
                file_data = f.read()
                msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=f"{os.path.basename(invoice_path)}")
        except FileNotFoundError:
            print(f"Invoice file not found at {invoice_path}")
            return

        # Send email
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(gmail_user, gmail_app_password)
                smtp.send_message(msg)

            print("Invoice sent successfully.")
            send_message_telegram(f"{name} Invoice sent successfully")

        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return

    else:
        print(f"{name} has no mailing list")

