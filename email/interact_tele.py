import sqlite3
import os
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Create an inline keyboard with buttons for each command
    keyboard = [
        [InlineKeyboardButton("Remove Invoice", callback_data='remove_invoice')],
        [InlineKeyboardButton("Update Amount", callback_data='update_amount')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send a message with the inline keyboard
    await update.message.reply_text(
        'Welcome! Choose an action:',
        reply_markup=reply_markup
    )

async def remove_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()  # Acknowledge the button click
    await update.callback_query.message.reply_text('Please enter invoice details to remove in format: Remove ClientName InvoiceNumber\n(e.g., Remove MetaFrontier 001)')
    context.user_data['expecting_remove'] = True

async def handle_remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('expecting_remove'):
        try:
            message_text = update.message.text
            message_text = message_text[len('Remove '):]
            client_name, invoice_no = message_text.split()

            conn = sqlite3.connect('invoices_pending.db')
            c = conn.cursor()
            
            # Check if invoice exists
            c.execute("SELECT * FROM invoices WHERE name = ? AND invoice_no = ?", (client_name, invoice_no))
            result = c.fetchone()
            
            if result:
                c.execute("DELETE FROM invoices WHERE name = ? AND invoice_no = ?", (client_name, invoice_no))
                conn.commit()
                await update.message.reply_text(f'Successfully removed invoice {invoice_no} for {client_name}')
            else:
                await update.message.reply_text(f'Invoice {invoice_no} for {client_name} not found')
            
            conn.close()
            context.user_data['expecting_remove'] = False
            
        except ValueError:
            await update.message.reply_text('Invalid format. Please use format: Remove ClientName InvoiceNumber')
    else:
        await update.message.reply_text('Click on Remove Invoice to remove an invoice')

async def update_amount(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.callback_query.answer()  # Acknowledge the button click
    await update.callback_query.message.reply_text('Please enter invoice details to update in format: Update ClientName InvoiceNumber NewAmount\n(e.g., Update MetaFrontier 001 5000)')
    context.user_data['expecting_update'] = True

async def handle_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.user_data.get('expecting_update'):
        try:
            message_text = update.message.text
            message_text = message_text[len('Update '):]
            client_name, invoice_no, new_amount = message_text.split()
            new_amount = float(new_amount)

            conn = sqlite3.connect('invoices_pending.db')
            c = conn.cursor()
            
            # Check if invoice exists
            c.execute("SELECT * FROM invoices WHERE name = ? AND invoice_no = ?", (client_name, invoice_no))
            result = c.fetchone()
            
            if result:
                c.execute("UPDATE invoices SET total_amount = ? WHERE name = ? AND invoice_no = ?", 
                         (new_amount, client_name, invoice_no))
                conn.commit()
                await update.message.reply_text(f'Successfully updated amount to {new_amount} for invoice {invoice_no} ({client_name})')
            else:
                await update.message.reply_text(f'Invoice {invoice_no} for {client_name} not found')
            
            conn.close()
            context.user_data['expecting_update'] = False
            
        except ValueError:
            await update.message.reply_text('Invalid format. Please use format: Update ClientName InvoiceNumber NewAmount')
    else:
        await update.message.reply_text('Click on Update Amount to update an invoice amount')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Handle button presses
    query = update.callback_query
    action = query.data

    if action == 'remove_invoice':
        await remove_invoice(update, context)
    elif action == 'update_amount':
        await update_amount(update, context)

def main() -> None:
    # Initialize the Bot
    bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

    # Create the Application and pass it your bot's token
    application = Application.builder().bot(bot).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))

    # Register handlers with more specific conditions
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)^REMOVE '), handle_remove))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)^UPDATE '), handle_update))
    application.add_handler(CallbackQueryHandler(button_handler))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == '__main__':
    main()
