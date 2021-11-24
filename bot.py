from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import Message
from manager import Manager

# Объект бота
bot = Bot(token=open("bot-token.txt", "r").read(), parse_mode=types.ParseMode.HTML)
# Диспетчер для бота
dp = Dispatcher(bot)
# Подключаем управляющего
MrB = Manager()

Messages = {
    'start':"Привет!",
    'access_denied':"Ой, кажется у тебя недостаточно прав для этого.",
    'help':"Здесь будет справка, когда нибудь.",
    'set_date':'Дата обновлена. Сейчас {date}',
    'set_date_error':'Ошибка. Дата {date} не распознана. Попробуйте записать в виде 7/11/21',
    'change_name':'Прощай, {old}, теперь я буду звать тебя {new}!',
    'set_name':'Привет {new}',
}

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    MrB.register(message.from_user.id)
    await message.reply(Messages['start'])

@dp.message_handler(state='*', commands=['setname', 'myname'])
async def process_reg_command(message: types.Message):
    res = MrB.setUserName(message.from_user.id, message.get_args())
    if res['old']:
        await message.answer(Messages['change_name'].format(old=res['old'], new=res['new']))
    else:
        await message.answer(Messages['set_name'].format(new=res['new']))
    
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(Messages['help'])

@dp.message_handler(state='*', commands=['setdate'])
async def process_setdate_command(message: types.Message):
    res = MrB.setDate(message.from_user.id, message.get_args())
    if res:
        await message.reply(Messages['set_date'].format(date=res))
    else:
        await message.reply(Messages['set_date_error'].format(date=message.get_args()))

@dp.message_handler(commands=['getusers'])
async def process_getusers_command(message: types.Message):
    res = MrB.getUsers(message.from_user.id)
    if res == -1:
        await message.answer(Messages['access_denied'])
    else:
        text = "<b>Список пользователей:</b>\n"
        for i in res:
            text += "Пользователь: {name}[{id}] \nС правами {right}\n".format(
                id=i['id'],name=i['name'],right=i['right'])
        await message.answer(text)

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
