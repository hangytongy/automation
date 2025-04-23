import invoice
import mail
from projects_list import projects
from post_telegram import send_photo_telegram
import os
from dotenv import load_dotenv

send_mail = False
send_tele = True


project = projects[1]


project_folder = f"invoices/{project['project']}"
if not os.path.exists(project_folder):
    os.makedirs(project_folder)


invoice_no, no_of_invoices = invoice.get_invoice_no(project)
start_date, end_date = invoice.get_start_end_date(project,no_of_invoices)
invoice_items = invoice.get_invoice_items(project,start_date,end_date)

client_name = project['client name']
client_addy = project['client addy']
client_alias = project['client alias']
no_of_teams = project['no of teams']
start_time = project['start time']
payment_type = project['payment_type']
payment_addy = project['payment_address']



doc_path = invoice.create_invoice(project_folder,client_name,client_addy,client_alias,invoice_no,invoice_items,no_of_teams,start_date,
                   end_date,start_time,payment_type,payment_addy)

if send_tele:
    caption = f"Invoice {client_alias}-{invoice_no} Generated"
    send_photo_telegram(doc_path, caption)

if send_mail:
    mail.send_email(project,end_date)