import requests
import datetime
import pytz
import telebot

token = "5326682533:AAHx4_7ke_U9VDOo7_OI-vhgkG_VKdUYIlw"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def start_command(message):
    bot.send_message(message.chat.id, f"Assalomaleykum, {message.from_user.first_name}. Telegram botimizga xush kelibsiz. Ushbu botda istalgan hududni ob-havosini bilib olishingiz mumkin.\n\n*Hudud nomini kiritishingiz mumkin*\n(misol uchun: Navoi)", parse_mode="Markdown")


@bot.message_handler(content_types=["text"])
def get_weather(message):
    code_to_smile = {
        "Clear": "Ochiq osmon. \U00002600",
        "Clouds": "Bulutli. \U00002601",
        "Rain": "Yomg'irli. \U00002614",
        "Drizzle": "Yog'ingarchilik. \U00002614",
        "Thunderstorm": "Momaqaldiroq. \U000026A1",
        "Snow": "Qor. \U0001F328",
        "Mist": "Tuman. \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid=b2b2ce6e7999964cf46c1849fe69edc0&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "⚠️"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        
        datetimenow = datetime.datetime.now(pytz.timezone('Asia/Tashkent')).strftime("%d-%m-%Y %H:%M:%S")
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]
        
        sunrise_timestamp = datetime.datetime.fromtimestamp(sunrise, tz=pytz.timezone('Asia/Tashkent')).strftime("%H:%M:%S")
        sunset_timestamp = datetime.datetime.fromtimestamp(sunset, tz=pytz.timezone('Asia/Tashkent')).strftime("%H:%M:%S")
        length_of_the_day  =  datetime.datetime.fromtimestamp(sunset, tz=pytz.timezone('Asia/Tashkent')) - datetime.datetime.fromtimestamp(sunrise, tz=pytz.timezone('Asia/Tashkent'))
        

        bot.send_message(message.chat.id, f"*** {datetimenow} ***\n\n*➡️ HUDUD:* ''' *{city}* '''\n\n🌡️ HARORAT: *{cur_weather}C°* {wd}\n☂️ NAMLIK: {humidity}%\n➡️ BOSIM: {pressure} mms\n💨 SHAMOL TEZLIGI: {wind} m/s\n🌇 QUYOSH CHIQISHI: *{sunrise_timestamp}*\n🌅 QUYOSH BOTISHI: *{sunset_timestamp}*\n🕢 KUN DAVOMIYLIGI: *{length_of_the_day}*\n\n***XAYRLI KUN***\n***😊DOIM OLLOH PANOHIDA BO'LING😊***", parse_mode="Markdown")

    except:
        bot.send_message(message.chat.id, "⚠️ HUDUD NOMINI TO'G'RI KIRITING ⚠️")

if __name__ == "__main__":
    bot.polling(none_stop=True)