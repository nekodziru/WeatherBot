# ░█████╗░██████╗░██████╗░██╗░░░██╗
# ██╔══██╗██╔══██╗██╔══██╗██║░░░██║    
# ███████║██████╦╝██║░░██║██║░░░██║
# ██╔══██║██╔══██╗██║░░██║██║░░░██║
# ██║░░██║██████╦╝██████╔╝╚██████╔╝
# ╚═╝░░╚═╝╚═════╝░╚═════╝░░╚═════╝░
# Developer @ABDU_UYGHUR, Copyright LTD 2022.
# ██╗░░░██╗██╗░░░██╗░██████╗░██╗░░██╗██╗░░░██╗██████╗░
# ██║░░░██║╚██╗░██╔╝██╔════╝░██║░░██║██║░░░██║██╔══██╗
# ██║░░░██║░╚████╔╝░██║░░██╗░███████║██║░░░██║██████╔╝
# ██║░░░██║░░╚██╔╝░░██║░░╚██╗██╔══██║██║░░░██║██╔══██╗
# ╚██████╔╝░░░██║░░░╚██████╔╝██║░░██║╚██████╔╝██║░░██║
# ░╚═════╝░░░░╚═╝░░░░╚═════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░╚═╝
import datetime
from turtle import forward
from matplotlib import animation
import requests
from config import weather_token, admin
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
markdown = """
    *bold text*
    _italic text_
    """
bot_token = '5411675687:AAHMw_RyJ-y9G_kj38tV09hgq8QHcoYN4vE'
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def process_start_command(message: types.Message):
    await message.answer_animation("https://t.me/svgpngforcoding/19")
    await message.reply(f"*Привет *" + str(message.from_user.first_name) + "\n*Напишите название населенного пункта, чтобы я показал погоду😊\n\n/help*", parse_mode='markdown')  

@dp.message_handler(commands=["help"])
async def help_command(message: types.Message):
    await message.reply(f"*Если вы заметили ошибку или у вас есть вопросы и предложения, свяжитесь с администратором😊: @ABDU_UYGHUR*", parse_mode='markdown')

@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Мелкий дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try: 
#api: документация AbduTools, API- документацию можете получать здесь:  https://openweathermap.org/api
        r = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={weather_token}&units=metric")
#Parsing json: Json переводим к Python   
        data = r.json()
#Настройка утилиты:
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = f"Посмотри в окно, не пойму что там за погода!"

        city_name = data["name"]
        cur_weather = data["main"]["temp"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])

#Настройка сообщений:
        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
              f"Погода в городе: {city_name}\n\nТемпература: {cur_weather}C° {wd}\n"
              f"Давление: {pressure} мм.рт.ст\nВлажность: {humidity}%\nВетер: {wind}\n\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n\n"
              f"*Спасибо за использование нашего бота🤩.Если заметили ошибку, обратитесь администратору: @ABDU_UYGHUR.*", parse_mode='markdown'
              )

#Если город неправильно прописан:
    except:
        await message.reply("\U00002620 Проверьте правильность названия города \U00002620")

if __name__ == '__main__':
    executor.start_polling(dp)
