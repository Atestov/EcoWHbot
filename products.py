import pandas as pd
import os.path

class Products():
    '''
    Класс для работы с товарами
    '''
    columns = ['date', 'price', 'name', 'available', 'reserve', 'freely']
    data = pd.DataFrame([],columns=columns)
    
    def __init__(self):
        self.Load()
            
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
        data['name'] = self._ReplaceSimilarCharacters_(data['name'])
        return data
        
    def Add(self, date, file):
        '''
        Добавляет записи за указанную дату.
        В отличие от Update не меняет существующие записи
        '''
        data = self._ExtractData_(date, file)
        self.data = pd.concat([self.data,data])
        self.Save()
        
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
        self.Save()
        
    def Save(self):
        self.data.to_csv(self._createDataFile_(), index=False)

    def Load(self):
        self.data = pd.read_csv(self._createDataFile_())

    def _ReplaceSimilarCharacters_(self, df):
        '''
        Замена похожих символов и исправление опечаток.
        На вход принимает DataFrame, возвращает обработанный DataFrame
        '''
        #В исходной базе 1с и соответственно выгрузке из неё много опечаток и разных написаний
        #Например размер горшка С25 может быть записан как С25, С 25, С25 см, С 25 см см

        # [ 'Что меняем' , 'на что меняем' ]
        replacement_rules = [
            ["P", "Р"], #Замена латинской P на русскую Р
            ["p", "р"], #Замена латинской P на русскую Р
            ["C", "С"], #Замена латинской C на русскую С
            ["C", "с"], #Замена латинской C на русскую С
            ["0 new см", "0 см new"], # Замена 300-400 new см на 300-400 см new
            ["см см", "см"], #"см см" на "см"
            [", см", ""] # С5, см на С5
        ]
        for i in replacement_rules:
            df = df.str.replace(i[0], i[1], regex = False)
        
        #[ r'Регулярное выражение', 'что нужно заменить в найденной подстроке', 'на что нужно заменить' ]
        replacement_rules = [
            [r'С[ ]{1,}\d'," ", ""], #C 25 -> C25
            [r'Р[ ]{1,}\d'," ", ""], #P 25 -> P25
            [r'\dсм', "см", " см"], #180см -> 180 см
            [r', ,', ", ,", ","], #, , -> ,
            [r' , '," , ", ", "], # ' , ' -> ", "
            [r'\)см', ")см", ")"], # (латинское название)см -> (латинское название)
            [r'\D\(', "(", " ("], # текст(лат. Название) -> текст (лат. Название)
            [r'С\d* см', " см", ""], # С25 см -> C25
            [r'С\d{1,},\d', ",", "."] # C7,5 -> C7.5
        ]
        for i in replacement_rules:
            df = df.str.replace(i[0], lambda x: x.group(0).replace(i[1], i[2]), regex = True)
            
        df = df.str.replace(r'\s{2,}', " ", regex = True) #Убираем множественные пробелы
        
        return df
