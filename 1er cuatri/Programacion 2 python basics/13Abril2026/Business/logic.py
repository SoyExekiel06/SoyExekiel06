from Data.dataHelper import DataHelper

class Logic:
    def __init__(self, user, dni):
        self.dni = dni
        self.user = user


    def validate(self):
        if self.dni.find(".") > 0 or self.dni.find(",") > 0:
            return False
        if self.dni.isdigit() == False:
            return False
        self.user = self.user.lower().strip()
        return True
    

    def check(self):
        dh = DataHelper()
        res = dh.getOne(self.dni, self.user)
        if res == False:
            return "No hay datos"
        if res == self.user:
            return "Hay match"
        else:
            return "No hay match"