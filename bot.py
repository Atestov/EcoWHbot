from aiogram import Bot, Dispatcher, executor, types
import pandas as pd
import os.path

# Объект бота
bot = Bot(token=open("bot-token.txt", "r").read())
# Диспетчер для бота
dp = Dispatcher(bot)

class Products():
    '''
    Класс для работы с товарами
    '''
    data = pd.DataFrame([],columns=['id', 'name', 'date', 'available', 'reserve', 'freely'])
    
    def __init__(self)
        sefl.data = pd.read_csv(_createDataFile_)
            
    def _createDataFile_()
        '''
        Функция создает csv файл для хранения данных если это необходимо.
        Возвращает путь к этому файлу
        '''
        dataFile = "data.csv"
        if not os.path.isfile(dataFile):
            pd.DataFrame([],columns=['id', 'name', 'date', 'available', 'reserve', 'freely']).to_csv(dataFile)
        return dataFile


if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
