import pycountryAdd commentMore actions
from countryinfo import CountryInfo

def get_country_data(user_input):
    user_input = user_input.strip().lower()

    # Try direct match first
    match = None
    for country in pycountry.countries:
        if (user_input == country.name.lower() or
            user_input == getattr(country, 'official_name', '').lower() or
            user_input == country.alpha_2.lower() or
            user_input == country.alpha_3.lower() or
            user_input in country.name.lower()):
            match = country
            break

    # If not found, return error
    if not match:
        return None, None, None

    # Get country info
    try:
        info = CountryInfo(match.name)
        flag = ''.join([chr(127397 + ord(c)) for c in match.alpha_2])
        details = f"""🌍 Country: {match.name}
🏛 Capital: {info.capital()}
📍 Region: {info.region()}
📚 Languages: {', '.join(info.languages())}
💰 Currency: {', '.join(info.currencies())}
👥 Population: {info.info().get('population', 'Unknown')}
📞 Calling Code: {', '.join(info.calling_codes())}
"""
        return flag, match.name, details
    except Exception as e:
        return '🇺🇳', match.name, "❌ Couldn't retrieve full info."

# Example usage
country = input("Enter country: ")
flag, name, info = get_country_data(country)
if flag:
    print(flag)
    print(info)
else:
    print("❌ I couldn't find that country. Please try a valid name.")
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler

TOKEN = "8088210734:AAFYLqqjYNhSDUdTWHQ2v11rmBsUVZ-sTws"
API_URL = "https://restcountries.com/v3.1/name/"

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "🌍 Welcome to the Country Info Bot!\n"
        "Send me a country name to get information and its flag.\n\n"
        "Example: France or france",
        parse_mode='Markdown'
    )

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
    # Get the first country from possible multiple results
    country = data[0]

    # Extract country information
    name = country.get('name', {}).get('common', 'N/A')
    official_name = country.get('name', {}).get('official', 'N/A')
    capital = ', '.join(country.get('capital', ['N/A']))
    region = country.get('region', 'N/A')
    subregion = country.get('subregion', 'N/A')
    population = f"{country.get('population', 0):,}"
    area = f"{country.get('area', 0):,} km²" if country.get('area') else 'N/A'
    languages = ', '.join(country.get('languages', {}).values()) if country.get('languages') else 'N/A'
    
    # Format currencies
    currencies = country.get('currencies', {})
    if currencies:
        currency_info = []
        for code, info in currencies.items():
            currency_info.append(f"{info['name']} ({info['symbol']})")
        currencies_str = ', '.join(currency_info)
    else:
        currencies_str = 'N/A'
    
    # Get flag URL
    flag_url = country.get('flags', {}).get('png', '')
    
    # Prepare response message
    message = (
        f"🇺🇳 *{name}* ({official_name})\n\n"
        f"*Capital:* {capital}\n"
        f"*Region:* {region} ({subregion})\n"
        f"*Population:* {population}\n"
        f"*Area:* {area}\n"
        f"*Languages:* {languages}\n"
        f"*Currencies:* {currencies_str}"
    )

    # Send message with flag photo
    if flag_url:
        await update.message.reply_photo(
            photo=flag_url,
            caption=message,
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(message, parse_mode='Markdown')

async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "ℹ️ Send any country name to get:\n"
        "- Basic information\n"
        "- Official flag image\n\n"
        "Examples:\nGermany\nbrazil\nsouth africa"
    )

def main():
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_country_info))
    
    # Start the Bot
    application.run_polling()

if name == 'main':
    main()
