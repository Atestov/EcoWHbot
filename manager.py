from datetime import datetime
from dateutil.parser import parse
from products import Products
from users import Users

class Manager():
    '''
    Класс Manager реализует взаимодействие пользователей с базой.
    Предостовляет методы для бота, но не логику бота.
    Методы возвращают: 
        -1: доступ запрещен
        True: операция выполнена успешно
        False: возникла ошибка
        Данные: если запрашивались данные
    '''
    product = Products()
    users = Users()

    def checkRight(self, user, operation):
        return self.users[user].hasRight(operation)

    def isBan(self, user):
        return not self.checkRight(user, 'access')

    def getDate(self, user):
        return self.users[user].getDate()
    
    def setDate(self, user, date):
        try:
            date = parse(date, dayfirst=len(date)>=4).date()
            # dayfirst определяет что идет раньше день или месяц. 
            # Предполагается что пользователи будут вводить дату в формате d m или d m y
            # дату в формате y m d определит неправильно. 
        except:
            return False
        self.users[user].setDate(date)
        self.users.save()
        return date.strftime('%d/%m/%Y')
    
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

    def search(self, user, request, data=False):
        if not self.checkRight(user, 'reading'):
            return -1

        date = self.getDate(user) if not date else date

        return self.product.search(date, request)

    def register(self, user):
        if not user in self.users:
            self.users.addUser(user)
            self.users.save()
        return True
    
    def getUsers(self, user):
        if not self.checkRight(user, 'admin'):
            return -1
        
        return [{'id':user.getID(), 'right':user.getUserRights(), 'name':user.getName()} for user in self.users]

    def setUserName(self, user, name):
        lastName = self.users[user].getName()
        self.users[user].setName(name)
        self.users.save()
        return {'old':lastName, 'new':name}
