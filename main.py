import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler,filters, MessageHandler, CallbackContext

OPENWEATHERMAP_API_KEY = '0444a702613ec2f5b525bf60d29ff2a0'


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я могу показать тебе текущую погоду. Просто отправь мне название города.')


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Отправь мне название города, чтобы узнать текущую погоду.')


def weather(update: Update, context: CallbackContext) -> None:
    city_name = update.message.text.strip()

    if not city_name:
        return update.message.reply_text("Пожалуйста, введите название города.")


    url = "http://api.openweathermap.org/data/2.5/weather"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        description = data['weather'][0]['description'].capitalize()
        wind_speed = data['wind']['speed']

        message = (
            f"Текущая погода в {city_name}:\n"
            f"Температура: {temp}°C\n"
            f"Ощущается как: {feels_like}°C\n"
            f"Погодные условия: {description}\n"
            f"Скорость ветра: {wind_speed} м/с"
        )

        update.message.reply_text(message)
    else:
        update.message.reply_text("Не удалось найти информацию о погоде для города . Попробуйте еще раз.")


def main() -> None:
    updater = Updater("8005207225:AAGCD09S5tyNdEQA-ceEK9SX5cWm298ErwA")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(filters.text & ~filters.command, weather))

    updater.start_polling()
    updater.idle()


    if __name__ == '__main__':
        while True:

            try:
                bot.polling(none_stop=True, interval=0)

            except Exception as e:
                print('Сработало исключние')

