import telebot
import random

TOKEN = "8088210734:AAFYLqqjYNhSDUdTWHQ2v11rmBsUVZ-sTws"  # Replace with your actual bot token
bot = telebot.TeleBot(TOKEN)

# List of motivational quotes
quotes = [
    "🌟 Believe in yourself and all that you are.",
    "💪 The harder you work for something, the greater you’ll feel when you achieve it.",
    "🚀 Don’t watch the clock; do what it does. Keep going.",
    "🔥 Push yourself, because no one else is going to do it for you.",
    "🎯 Success doesn’t just find you. You have to go out and get it."
]

# /start command handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(f"Received /start from {message.from_user.username}")
    bot.reply_to(message, "👋 Hello! I'm your bot running with polling.\nType /quote to get a motivational quote.")

# /quote command handler
@bot.message_handler(commands=['quote'])
def send_quote(message):
    quote = random.choice(quotes)
    print(f"Sent quote to {message.from_user.username}")
    bot.reply_to(message, quote)

# Echo handler
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    print(f"Received message: {message.text} from {message.from_user.username}")
    bot.reply_to(message, message.text)

if __name__ == "__main__":
    print("🤖 Bot is running using polling...")
    bot.infinity_polling()
