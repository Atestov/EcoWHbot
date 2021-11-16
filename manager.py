from numpy import product
from products import Products
from users import Users

class Manager():
    '''
    Класс Manager реализует взаимодействие пользователей с базой.
    Предостовляет методы для бота, но не логику бота.
    Методы возвращают: 
        -1: доступ запрещен
        True: операция выполнена успешно
        Данные: если запрашивались данные
    '''
    product = Product()
    users = Users()

    def checkRight(self, user, operation):
        return self.users[user].hasRight(operation)

    def isBan(self, user):
        return not self.checkRight(user, 'access')

    def getDate(self, user):
        return users[user].getDate()
    
    def addProducts(self, user, file, date=False):
        if not self.checkRight(user, 'change'):
            return -1

        date = self.getDate(user) if not date else date

        self.product.Add(date, file)
        return True

    def updateProducts(self, user, file, date = False, rewrite = True):
        if not self.checkRight(user, 'change'):
            return -1

        date = self.getDate(user) if not date else date

        self.product.Update(date, file, rewrite)
        return True

    def search(self, user, request, data=False]):
        if not self.checkRight(user, 'reading'):
            return -1

        date = self.getDate(user) if not date else date

        return self.product.search(date, request)
