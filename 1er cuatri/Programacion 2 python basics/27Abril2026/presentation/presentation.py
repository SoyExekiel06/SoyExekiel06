import getpass
from business.business import LoginHelper


class App:
    #resuelve que el input de los passwords no sean numeros visibles, sino puntitos.
    def __init__(self):
        self.loginHelper = LoginHelper()

    def registrarUsuario(self):

        try:

            username = input("Ingrese el nuevo nombre de usuario:\n")
            username = self.loginHelper.sanitize(username)

            #Doble ingreso de pw para verificacion
            pwd1 = getpass.getpass(prompt="Ingrese su password:\n")#No te muestra nada pero sí ingresa los caracteres
            pwd2 = getpass.getpass(prompt="Repita la password:\n")
            self.loginHelper.checkEqPwd(pwd1, pwd2)
            self.loginHelper.prepareAndStorePwd(username,pwd1)
        
        except Exception as e:
            print("Error: {}".format(e))


    def iniciarSesion(self,):
        try:
            username = input("Ingrese el nombre de usuario:\n")
            username = self.loginHelper.sanitize(username)
            pwd = getpass.getpass(prompt="Ingrese su password:\n")#No te muestra nada pero sí ingresa los caracteres
            self.loginHelper.checkUserAndPwd(username,pwd)
            print("Bienvenido, {}".format(username)) #Si ingresa todo bien, te saluda.
        except ValueError as e:
            print("Error: {}".format(e.args[0]))
            
    def menu(self):
        print(20*"-","Badass Log-in",20*"-")
        print("Ingrese el numero correspondiente a la accion que desea realizar")
        print("1 - Iniciar Sesion")
        print("2 - Crear Usuario")
        print("0 - Salir")

        opcion = input().strip()
        match opcion:
            case "1":
                self.iniciarSesion()
                return False
            case "2":
                self.registrarUsuario()
                return True
            case "0":
                print("Chau!")
                return False
            case _ :
                print("Opcion incorrecta")
                return True
