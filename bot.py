from aiogram import Bot, Dispatcher, executor, types
from products import Products

# Объект бота
bot = Bot(token=open("bot-token.txt", "r").read())
# Диспетчер для бота
dp = Dispatcher(bot)

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
