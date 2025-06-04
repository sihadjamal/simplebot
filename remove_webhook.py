import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "8088210734:AAFYLqqjYNhSDUdTWHQ2v11rmBsUVZ-sTws"
API_URL = "https://restcountries.com/v3.1/name/"

# /start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🌍 Welcome to the Country Info Bot!\n"
        "Send me a country name to get information and its flag.\n\n"
        "Example: France or france"
    )

# /help command
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "ℹ️ Send any country name to get:\n"
        "- Basic information\n"
        "- Official flag image\n\n"
        "Examples:\nGermany\nBrazil\nSouth Africa"
    )

# Handles country name text
async def get_country_info(update: Update, context: CallbackContext):
    country_name = update.message.text.strip()
    if not country_name:
        await update.message.reply_text("Please enter a country name.")
        return

    response = requests.get(f"{API_URL}{country_name}")
    
    if response.status_code == 404:
        await update.message.reply_text("❌ Country not found. Please check the spelling and try again.")
        return
    elif response.status_code != 200:
        await update.message.reply_text("⚠️ Service unavailable. Please try again later.")
        return

    data = response.json()
    country = data[0]

    name = country.get('name', {}).get('common', 'N/A')
    official_name = country.get('name', {}).get('official', 'N/A')
    capital = ', '.join(country.get('capital', ['N/A']))
    region = country.get('region', 'N/A')
    subregion = country.get('subregion', 'N/A')
    population = f"{country.get('population', 0):,}"
    area = f"{country.get('area', 0):,} km²" if country.get('area') else 'N/A'
    languages = ', '.join(country.get('languages', {}).values()) if country.get('languages') else 'N/A'

    currencies = country.get('currencies', {})
    if currencies:
        currency_info = [f"{info.get('name', '')} ({info.get('symbol', '')})" for info in currencies.values()]
        currencies_str = ', '.join(currency_info)
    else:
        currencies_str = 'N/A'

    flag_url = country.get('flags', {}).get('png', '')

    message = (
        f"🇺🇳 *{name}* ({official_name})\n\n"
        f"*Capital:* {capital}\n"
        f"*Region:* {region} ({subregion})\n"
        f"*Population:* {population}\n"
        f"*Area:* {area}\n"
        f"*Languages:* {languages}\n"
        f"*Currencies:* {currencies_str}"
    )

    if flag_url:
        await update.message.reply_photo(
            photo=flag_url,
            caption=message,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(message, parse_mode='Markdown')

# Main runner
def main():
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_country_info))
    
    print("🤖 Bot is running...")
    application.run_polling()

# Entry point
if __name__ == "__main__":
    main()
