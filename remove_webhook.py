import pycountry
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
