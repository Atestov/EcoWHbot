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
    columns = ['id', 'name', 'date', 'available', 'reserve', 'freely']
    data = pd.DataFrame([],columns=columns)
    
    def __init__(self):
        sefl.data = pd.read_csv(self._createDataFile_)
            
    def _createDataFile_(self):
        '''
        Функция создает csv файл для хранения данных если это необходимо.
        Возвращает путь к этому файлу
        '''
        dataFile = "data.csv"
        if not os.path.isfile(dataFile):
            pd.DataFrame([],columns=self.columns).to_csv(dataFile)
        return dataFile

    def Add(self, date, file):
        file = pd.read_excel(file)
        # У файлов с отстаками плавающее начало таблицы.
        #Иногда есть заголовок, иногда нет. Ищем начало по слову Цена
        column = 1
        while file[file.columns[0][column]] != "Цена":
            column += 1
        column += 2 #После строки с ценой всегда идет пустая строка
                   
        appendData = file.iloc[column:, [0,1,-3,-2,-1]]
        #Особенность excel файла в непостоянном количестве столбцов.
        #Иногда есть столбец еденица измерения. Но нужные данные всегда в 1, 2 и последних трех столбцах
        self.data.append(appendData, ignore_index = True)

    def save():
        self.data.to_csv(self._createDataFile_())
        
if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
