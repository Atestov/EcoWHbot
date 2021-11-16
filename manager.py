from numpy import product
from products import Products
from users import Users

class Manager():
    '''
    Класс Manager реализует взаимодействие пользователей с базой.
    Предостовляет методы для бота, но не логику бота.
    '''
    product = Product()
    users = Users()

    def checkRight(self, user, operation):
        return self.users[user].hasRight(operation)

    def isBan(self, user):
        return not self.checkRight(user, 'access')
    
    def addProducts(self, user, date, file):
        if not self.checkRight(user, 'change'):
            return False
        
        self.product.Add(date, file)
        return True

    def updateProducts(self, user, date, file, rewrite = True):
        if not self.checkRight(user, 'change'):
            return False
        
        self.product.Update(date, file, rewrite)
        return True
