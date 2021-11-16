from aiogram import Bot, Dispatcher, executor, types
from manager import Manager

# Объект бота
bot = Bot(token=open("bot-token.txt", "r").read())
# Диспетчер для бота
dp = Dispatcher(bot)
# Подключаем управляющего
MrB = Manager()

Messages = {
    'start':"Привет!",
    'access_denied':"Ой, кажется у тебя недостаточно прав для этого.",
    'help':"Здесь будет справка, когда нибудь.",
    'set_date':'Дата обновлена. Сейчас {date}',
}

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    MrB.register(message.from_user.id)
    await message.reply(Messages['start'])


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(Messages['help'])

@dp.message_handler(state='*', commands=['setdate'])
async def process_setdate_command(message: types.Message):
    MrB.setDate(message.from_user.id, message.get_args())
    await message.reply(Messages['set_date'].format(date=message.get_args()))

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
