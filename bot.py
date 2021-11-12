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
    columns = ['date', 'price', 'name', 'available', 'reserve', 'freely']
    data = pd.DataFrame([],columns=columns)
    
    def __init__(self):
        self.load()
            
    def _createDataFile_(self):
        '''
        Функция создает csv файл для хранения данных если это необходимо.
        Возвращает путь к этому файлу
        '''
        dataFile = "data.csv"
        if not os.path.isfile(dataFile):
            pd.DataFrame([],columns=self.columns).to_csv(dataFile, index=False)
        return dataFile

    def _ExtractData_(self, date, file):
        file = pd.read_excel(file)
        # У файлов с отстаками плавающее начало таблицы.
        #Иногда есть заголовок, иногда нет. Ищем начало по слову Цена
        column = 0
        while file[file.columns[0]][column] != "Цена":
            column += 1
        column += 2 #После строки с ценой всегда идет пустая строка
                   
        data = file.iloc[column:, [0,1,-3,-2,-1]]
        #Особенность excel файла в непостоянном количестве столбцов.
        #Иногда есть столбец еденица измерения. Но нужные данные всегда в 1, 2 и последних трех столбцах
        data = data.fillna(0)#Nan -> 0
        data.insert(0, "date", date) #Вставка даты
        data.columns = self.columns
        return data
        
    def Add(self, date, file):
        '''
        Добавляет записи за указанную дату.
        В отличие от Update не меняет существующие записи
        '''
        data = self._ExtractData_(date, file)
        self.data = pd.concat([self.data,data])

    def Update(self, date, file, rewriteAll = True):
        '''
        Обновляет записи за определенную дату.
        Если параметр rewriteAll = True то полностью заменяет записи за указанную дату
        иначе только перезаписывает совпадающие записи
        '''
        if rewriteAll:
            self.data = self.data.loc[self.data['date'] != date]
        data = self._ExtractData_(date, file)
        #Добавляем все записи и удаляем дубликаты по дате и названию
        self.data = pd.concat([self.data, data]).drop_duplicates(['date','name'], keep='last')
        
    def save(self):
        self.data.to_csv(self._createDataFile_(), index=False)

    def load(self):
        self.data = pd.read_csv(self._createDataFile_())
        
if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
