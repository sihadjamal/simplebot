import telebot
import pycountry
from countryinfo import CountryInfo

TOKEN = "8088210734:AAFYLqqjYNhSDUdTWHQ2v11rmBsUVZ-sTws"  # Replace with your bot token
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🌍 Send me any country name and I’ll tell you about it!")

@bot.message_handler(func=lambda message: True)
def country_info(message):
    country_name = message.text.strip()
    try:
        country = pycountry.countries.get(name=country_name) or \
                  pycountry.countries.search_fuzzy(country_name)[0]

        info = CountryInfo(country.name)
        capital = info.capital()
        population = info.info().get("population", "Unknown")
        currencies = ", ".join(info.currencies())
        languages = ", ".join(info.languages())
        region = info.region()
        subregion = info.subregion()

        # Country flag emoji via Unicode Regional Indicator Symbols
        flag = ''.join([chr(127397 + ord(c)) for c in country.alpha_2.upper()])

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
        bot.reply_to(message, "❌ I couldn't find that country. Please try a valid name.")

if __name__ == "__main__":
    print("🌐 Country info bot is running...")
    bot.infinity_polling()
