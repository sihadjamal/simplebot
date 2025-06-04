import telebotAdd commentMore actions
import pycountry
from countryinfo import CountryInfo

TOKEN = "8088210734:AAFYLqqjYNhSDUdTWHQ2v11rmBsUVZ-sTws"  # Replace with your actual bot token
bot = telebot.TeleBot(TOKEN)

def get_flag_emoji(country_code):
    # Convert country alpha_2 code to regional indicator symbols (flag emoji)
    return ''.join(chr(127397 + ord(c)) for c in country_code.upper())

def format_population(pop):
    try:
        return f"{int(pop):,}"
    except:
        return "Unknown"

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user.username or message.from_user.first_name or "there"
    bot.reply_to(message, f"🌍 Hello @{user}! Send me any country name and I'll provide detailed info about it!")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message,
        "📝 *How to use this bot:*\n"
        "Simply send me the name of any country, and I'll reply with its capital, population, languages, currencies, and region.\n\n"
        "Commands:\n"
        "/start - Welcome message\n"
        "/help - This help message\n"
        "/about - About this bot",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(message,
        "🤖 *Country Info Bot*\n"
        "Built with Python, pycountry, and CountryInfo.\n"
        "Get quick facts and the flag emoji for any country.\n\n"
        "Created by YourName\n"
        "Source: https://github.com/yourgithubrepo",
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: True)
def country_info(message):
    country_name = message.text.strip()
    try:
        # Try exact match first
        country = pycountry.countries.get(name=country_name)
        # If not found, do fuzzy search for partial or similar names
        if not country:
            country = pycountry.countries.search_fuzzy(country_name)[0]

        info = CountryInfo(country.name)
        capital = info.capital() or "Unknown"
        population = format_population(info.info().get("population", "Unknown"))
        currencies = ", ".join(info.currencies()) if info.currencies() else "Unknown"
        languages = ", ".join(info.languages()) if info.languages() else "Unknown"
        region = info.region() or "Unknown"
        subregion = info.subregion() or "Unknown"
        flag = get_flag_emoji(country.alpha_2)

        reply = (
            f"{flag} *{country.name}*\n"
            f"🌆 Capital: {capital}\n"
            f"🌍 Region: {region} ({subregion})\n"
            f"🗣️ Languages: {languages}\n"
            f"💰 Currencies: {currencies}\n"
            f"👥 Population: {population}"
        )

        bot.reply_to(message, reply, parse_mode='Markdown')

    except Exception as e:
        bot.reply_to(message, "❌ I couldn't find that country. Please check the spelling and try again.")

if __name__ == "__main__":
    print("🌐 Country Info Bot is running...")
    bot.infinity_polling()
