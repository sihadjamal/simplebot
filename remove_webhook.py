import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

TOKEN = "8088210734:AAFYLqqjYNhSDUdTWHQ2v11rmBsUVZ-sTws"
API_URL = "https://restcountries.com/v3.1/name/"

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🌍 Welcome to the Country Info Bot!\n"
        "Send me a country name and I'll reply with its flag and information.\n\n"
        "Example: Japan, iran, germany"
    )

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "ℹ️ Type any country name to receive:\n"
        "- Country flag\n"
        "- Capital\n"
        "- Region, Population, Area\n"
        "- Languages and Currencies\n\n"
        "✅ Try: italy, turkey, usa"
    )

async def get_country_info(update: Update, context: CallbackContext):
    country_name = update.message.text.strip()

    try:
        response = requests.get(f"{API_URL}{country_name}?fullText=false")
        if response.status_code != 200:
            raise Exception("Country not found")

        country = response.json()[0]

        # Flag
        flag_url = country.get("flags", {}).get("png", "")
        # Country info
        name = country.get("name", {}).get("common", "N/A")
        official = country.get("name", {}).get("official", "N/A")
        capital = ', '.join(country.get("capital", ["N/A"]))
        region = country.get("region", "N/A")
        subregion = country.get("subregion", "N/A")
        population = f"{country.get('population', 0):,}"
        area = f"{country.get('area', 0):,} km²"
        languages = ', '.join(country.get("languages", {}).values())
        
        currencies_data = country.get("currencies", {})
        currencies = ', '.join(
            [f"{v['name']} ({v.get('symbol', '')})" for v in currencies_data.values()]
        )

        message = (
            f"🏳️ *{name}* ({official})\n\n"
            f"🏛️ *Capital:* {capital}\n"
            f"🌍 *Region:* {region} ({subregion})\n"
            f"👥 *Population:* {population}\n"
            f"📏 *Area:* {area}\n"
            f"🗣 *Languages:* {languages or 'N/A'}\n"
            f"💰 *Currencies:* {currencies or 'N/A'}"
        )

        if flag_url:
            await update.message.reply_photo(photo=flag_url, caption=message, parse_mode='Markdown')
        else:
            await update.message.reply_text(message, parse_mode='Markdown')

    except Exception as e:
        await update.message.reply_text("❌ I couldn't find that country. Please check the name and try again.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_country_info))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
