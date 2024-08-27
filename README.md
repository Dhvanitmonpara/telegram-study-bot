# 📚 Study Bot

**Study Bot** ([@Studybca_bot](https://t.me/Studybca_bot)) is a Telegram bot designed to assist users with study-related resources, offering contact information and study tips. Administrators can manage PDFs that users can retrieve by using specific keywords.

---

## 🌟 Features

- **👋 Welcome Message:** Automatically greets users with a friendly welcome message when they initiate a chat with the bot.
- **🛠️ Help Menu:** Provides a comprehensive list of commands to guide users in interacting with the bot.
- **📖 Study Tips:** Offers valuable study advice to help users stay focused and motivated.
- **📞 Contact Information:** Shares contact details and social media links for additional support.
- **📂 PDF Management:** Allows admins to add PDFs to a database, retrievable by users through specific keywords.
- **🤖 AI-Powered Responses:** Automatically retrieves and sends PDFs based on user input that matches keywords.

---

## 🚀 Commands

- `/start` - Begin your interaction with the bot.
- `/helps` - Display the help menu with available commands.
- `/content` - Receive study tips and strategies.
- `/contact` - Get contact details and social media links.
- `/addpdf <keyword> <file_path>` - **(Admin Only)** Add a PDF to the bot's database with a specific keyword.

---

## 📋 Requirements

- **Python 3.8+**
- `python-telegram-bot` library
- `python-dotenv` library
- `sqlite3` (bundled with Python)

---

## 🛠️ Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/study-bot.git
   cd study-bot
   ```

2. **Install the required packages:**
   ```bash
   pip install python-telegram-bot python-dotenv
   ```

3. **Create a `.env` file** in the project directory and add your bot’s token and admin ID:
   ```env
   TOKEN=your_telegram_bot_token
   ADMIN_ID=your_telegram_id
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

---

## 🗂️ Database

The bot uses **SQLite** to store PDFs and their associated keywords. A database file, `bot_database.db`, is created automatically when the bot runs.

---

## 💡 Usage

1. **Start the bot** by typing `/start`.
2. **View commands** using `/helps`.
3. **Add PDFs** using the `/addpdf` command, specifying a keyword and file path.
4. **Retrieve PDFs** by typing relevant keywords in the chat.

---

## 🤝 Contribution

Contributions are welcome! Feel free to open issues or submit pull requests. Please ensure your code adheres to the project’s coding standards.

---

