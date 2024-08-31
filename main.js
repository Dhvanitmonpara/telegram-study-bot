const TelegramBot = require('node-telegram-bot-api');
const sqlite3 = require('sqlite3').verbose();
const dotenv = require('dotenv');

dotenv.config();

const TOKEN = process.env.TOKEN;
const ADMIN_ID = parseInt(process.env.ADMIN_ID, 10);

const bot = new TelegramBot(TOKEN, { polling: true });

// Initialize the database
const db = new sqlite3.Database('bot_database.db');

bot.onText(/\/start/, (msg) => {
    bot.sendMessage(msg.chat.id, "Hello! Welcome to Study Bot");
});

bot.onText(/\/help/, (msg) => {
    const helpMessage = `
    Hi there! I'm Telegram Bot created by Sankalp. Please follow these commands:-
    
    /start - to start the conversation
    /content - Information about ME
    /contact - Information about contact
    /help - to get this help menu
    
    I hope this helps you :)
    `;
    bot.sendMessage(msg.chat.id, helpMessage);
});

bot.onText(/\/content/, (msg) => {
    const contentMessage = `
    Create a focused study environment, set clear goals, and use active learning techniques. Take regular breaks to avoid burnout. Prioritize sleep and stay organized with a planner. Don't hesitate to seek help when needed. Remember, consistent effort and smart strategies are key to academic success.
    `;
    bot.sendMessage(msg.chat.id, contentMessage);
});

bot.onText(/\/contact/, (msg) => {
    const contactMessage = `
    **Contact Us:**

    * **Phone:** +91 123 456 7890
    * **Email:** [email protected]
    * **Address:** Your Company, Your City, India

    **Social Media:** [Links to your social media profiles]

    **Hours:** Mon-Fri 9-5, Sat 10-2, Sun Closed
    `;
    bot.sendMessage(msg.chat.id, contactMessage);
});

let pdfKeyword = null;

bot.onText(/\/addpdf (.+)/, (msg, match) => {
    const chatId = msg.chat.id;
    const userId = msg.from.id;

    bot.getChatAdministrators(chatId).then((admins) => {
        const adminIds = admins.map(admin => admin.user.id);

        if (!adminIds.includes(userId)) {
            bot.sendMessage(chatId, "You are not authorized to use this command.");
            return;
        }

        pdfKeyword = match[1].toLowerCase();
        bot.sendMessage(chatId, "Please send the PDF file now.");
    });
});

bot.on('document', (msg) => {
    if (!pdfKeyword) {
        bot.sendMessage(msg.chat.id, "Please use the /addpdf command first to provide a keyword.");
        return;
    }

    const fileId = msg.document.file_id;
    const fileMimeType = msg.document.mime_type;

    if (fileMimeType === "application/pdf") {
        bot.getFile(fileId).then((file) => {
            const fileStream = bot.downloadFile(fileId, './');

            let chunks = [];
            fileStream.on('data', (chunk) => {
                chunks.push(chunk);
            });

            fileStream.on('end', () => {
                const fileBuffer = Buffer.concat(chunks);

                db.run("INSERT INTO pdfs (keyword, file_data) VALUES (?, ?)", [pdfKeyword, fileBuffer], function(err) {
                    if (err) {
                        bot.sendMessage(msg.chat.id, `An error occurred: ${err.message}`);
                    } else {
                        bot.sendMessage(msg.chat.id, `PDF added with keyword '${pdfKeyword}'.`);
                    }
                });

                pdfKeyword = null;
            });
        });
    } else {
        bot.sendMessage(msg.chat.id, "Please upload a PDF file.");
    }
});

bot.on('message', (msg) => {
    const userText = msg.text.toLowerCase();

    if (userText.includes('note') || userText.includes('notes')) {
        db.get("SELECT file_data FROM pdfs WHERE ? LIKE '%' || keyword || '%'", userText, (err, row) => {
            if (err) {
                bot.sendMessage(msg.chat.id, `An error occurred: ${err.message}`);
            } else if (row && row.file_data) {
                bot.sendDocument(msg.chat.id, row.file_data, { filename: "document.pdf" });
            } else {
                bot.sendMessage(msg.chat.id, "No PDF found for your query.");
            }
        });
    }
});
