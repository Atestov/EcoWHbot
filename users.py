import os.path
import pickle
from datetime import date, time, timedelta

class Users:
    '''
    Класс для работы с пользователями. 
    '''
    List = {} #Ассоциативный массив 'id пользователя' : класс user
    right = ['access', 'reading', 'change', 'admin']
    #'access' - доступ к боту, 'reading' - доступ к базе товаров,
    #'change' - доступ к добавлению товаров, 'admin' - управление правами пользователей и ботом

    class User:
        id = ""
        curDate = date.today()
        right = ['access']

        def __init__(self, id) -> None:
            self.id = id
        
        def __str__(self) -> str:
            return self.id
        
        def __repr__(self):
            return str(self.id)
        
        def setDate(self, date):
            self.curDate = date

        def getDate(self):
            return self.curDate

        def getID(self):
            return self.id

        def __add__(self, count):
            self.curDate += timedelta(days=count)
        
        def __sub__(self, count):
            self.curDate -= timedelta(days=count)

        def setRight(self, right):
            '''Устанавливает права пользователя'''
            self.right = right

        def addRight(self, right):
            '''Добавляет определенное право пользователю'''
            if not right in self.right:
                self.right.append(right)
        
        def removeRight(self, right):
            '''Отнимает определенное право у пользователя'''
            if right in self.right:
                self.right.remove(right)
        
        def getUserRights(self):
            return self.right

        def hasRight(self, right):
            return right in self.right
    
    def __init__(self) -> None:
        self.load()

    def __getstate__(self) -> dict:
        return self.List

    def __setstate__(self, state: dict):
        self.List = state

    def addUser(self, id):
        self.List[id] = Users.User(id)

    def delUser(self, id):
        del(self.List[id])

    def setDate(self, date):
        '''Устанавливает дату для всех пользователей'''
        for user in self:
            user.setDate(date)

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

    def __getitem__(self, i):
        #Переопределяем для того что бы можно было писать users[num] вместо users.List[num]
        return self.List[i]
    
    def __iter__(self):
        return (self.List[i] for i in self.List.keys())
