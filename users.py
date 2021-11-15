import os.path
import pickle
from typing import List

class Users:
    List = {} #Ассоциативный массив 'id пользователя' : класс user

    class User:
        #Как таковой класс User не нужен. Я добавляю его на случай если потребуется расширить список хранимых данных о пользователе
        id = ""

        def __init__(self, id) -> None:
            self.id = id
        
        def __str__(self) -> str:
            return self.id
        
        def __repr__(self):
            return str(self.id)
    
    def __init__(self) -> None:
        self.load()

    def __getstate__(self) -> dict:
        return self.List

    def __setstate__(self, state: dict):
        self.List = state

    def addUser(self, id):
        self.List[id] = Users.User(id)

    def _getDataFile_(self):
        '''
        Возвращает путь к файлу с данными пользователей
        '''
        dataFile = "users.pkl"
        if not os.path.isfile(dataFile):
            pickle.dump({}, open(dataFile, "wb"))
        return dataFile

    def load(self):
        with open(self._getDataFile_(), "rb") as fp:
            self.List = pickle.load(fp)
        
    def save(self):
        with open(self._getDataFile_(), "wb") as fp:
            pickle.dump(self.List, fp)

    def __repr__(self):
        return str(self.List)
