import telegram.ext
from telegram import Update, Document
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import sqlite3

load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Welcome to Study Bot")

async def helps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '''
        Hi there! I'm Telegram Bot created by Sankalp. Please follow these commands:-
        
        /start - to start the conversation
        /content - Information about ME
        /contact - Information about contact
        /help - to get this help menu
        
        I hope this helps you :)
        '''
    )

async def content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '''
        Create a focused study environment, set clear goals, and use active learning techniques. Take regular breaks to avoid burnout. Prioritize sleep and stay organized with a planner. Don't hesitate to seek help when needed. Remember, consistent effort and smart strategies are key to academic success.
        '''
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '''
        **Contact Us:**

        * **Phone:** +91 123 456 7890
        * **Email:** [email protected]
        * **Address:** Your Company, Your City, India

        **Social Media:** [Links to your social media profiles]

        **Hours:** Mon-Fri 9-5, Sat 10-2, Sun Closed
        '''
    )

async def add_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id

    chat_admins = await context.bot.get_chat_administrators(chat_id)
    admin_ids = [admin.user.id for admin in chat_admins]

    if user_id not in admin_ids:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    
    try:
        keyword = context.args[0].lower()
        context.user_data['pdf_keyword'] = keyword
        await update.message.reply_text("Please send the PDF file now.")
    except IndexError:
        await update.message.reply_text("Please provide a keyword.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'pdf_keyword' not in context.user_data:
        await update.message.reply_text("Please use the /addpdf command first to provide a keyword.")
        return

    keyword = context.user_data.pop('pdf_keyword')  
    file = update.message.document

    if file.mime_type == "application/pdf":
        try:
            file_data = await file.get_file()
            file_bytes = await file_data.download_as_bytearray()

            conn = sqlite3.connect('bot_database.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pdfs (keyword, file_data) VALUES (?, ?)", (keyword, file_bytes))
            conn.commit()
            conn.close()

            await update.message.reply_text(f"PDF added with keyword '{keyword}'.")
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {e}")
    else:
        await update.message.reply_text("Please upload a PDF file.")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
 

    

    if 'note' in user_text or 'notes' in user_text:
        conn = sqlite3.connect('bot_database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT file_data FROM pdfs WHERE ? LIKE '%' || keyword || '%' AND (instr(?, ' note') > 0 OR instr(?, ' notes') > 0)", (user_text, user_text, user_text))
        result = cursor.fetchone()
        conn.close()

        if result:
            pdf_data = result[0]
            if pdf_data:
                await update.message.reply_document(document=pdf_data, filename="document.pdf")
            else:
                await update.message.reply_text("The file associated with this keyword no longer exists in the database.")
        else:
            await update.message.reply_text("No PDF found for your query.")



application = Application.builder().token(TOKEN).build()


application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('help', helps))
application.add_handler(CommandHandler('content', content))
application.add_handler(CommandHandler('contact', contact))
application.add_handler(CommandHandler('addpdf', add_pdf))


application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
application.add_handler(MessageHandler(filters.Document.ALL, handle_document))


application.run_polling()