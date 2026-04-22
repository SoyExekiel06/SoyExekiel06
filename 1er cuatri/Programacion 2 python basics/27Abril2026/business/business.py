import bcrypt
from data.dataHelper import dataHelper

class LoginHelper:
    def __init__(self):
            self.dataHelper = dataHelper()

    def sanitize(self, text):
        return text # TODO completar nosotros con la sanitizacion correspondiente del text, sin espacios, pasar a minisculas, sin simbolos no permitidos, etc...
    

    def checkEqPwd(self, pwd1, pwd2): #check equal passwords
        pwd1 = pwd1.strip()
        pwd2 = pwd2.strip()
        if pwd1 == pwd2:
            return
        else:
            raise ValueError("Las passwords no coinciden") # le tiramos un error de valores
        
    def prepareAndStorePwd(self,username,pwd): #disparamos el proceso q hashea el pwd y se guardan los archvos serializados
        codedPwd = pwd.encode('utf-8')
        hashedPwd = bcrypt.hashpw(codedPwd, bcrypt.gensalt())
        self.dataHelper.addUser(username, hashedPwd.decode('utf-8'))#la password se tiene que pasar codificada en utf-8 para q json permita su serializacion

    def checkUserAndPwd(self, username, pwd):
        hashedpwd = self.dataHelper.getUser(username)
        if hashedpwd is None:
            raise ValueError("Usuario inexistente")#No esta bueno darle tanta informacion a un posible atacante, entonces mejor poner invalido
        if bcrypt.checkpw(pwd.encode('utf-8'), hashedpwd.encode('utf-8')):
            return "OK"
        else:
            raise ValueError("Password Incorrecto")