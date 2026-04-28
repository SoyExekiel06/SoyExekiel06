import getpass
from tabulate import tabulate
from business.Usuarios import LoginHelper
 
 
class App:
    def __init__(self):
        self.loginHelper = LoginHelper()
        self.usuarioActivo = None  # guarda el username tras login exitoso
 
    def registrarUsuario(self):
        try:
            username = input("Ingrese el nuevo nombre de usuario:\n")
            username = self.loginHelper.sanitize(username)
            pwd1 = getpass.getpass(prompt="Ingrese su password:\n")
            pwd2 = getpass.getpass(prompt="Repita la password:\n")
            self.loginHelper.checkEqPwd(pwd1, pwd2)
            self.loginHelper.prepareAndStorePwd(username, pwd1)
            print(f"Usuario '{username}' creado correctamente.")
        except Exception as e:
            print("Error: {}".format(e))
 
    def iniciarSesion(self):
        try:
            username = input("Ingrese el nombre de usuario:\n")
            username = self.loginHelper.sanitize(username)
            pwd = getpass.getpass(prompt="Ingrese su password:\n")
            self.loginHelper.checkUserAndPwd(username, pwd)
            self.usuarioActivo = username
            print("Bienvenido, {}".format(username))
        except ValueError as e:
            print("Error: {}".format(e.args[0]))
 
    def abrirCuenta(self):
        if not self.usuarioActivo:
            print("Debe iniciar sesion primero.")
            return
        try:
            moneda = input("Ingrese el codigo de moneda (ej: USD, ARS, EUR):\n")
            self.loginHelper.abrir_cuenta(self.usuarioActivo, moneda)
            print(f"Cuenta en {moneda.strip().upper()} abierta correctamente.")
        except ValueError as e:
            print("Error: {}".format(e.args[0]))
 
    def listarCuentas(self):
        if not self.usuarioActivo:
            print("Debe iniciar sesion primero.")
            return
        filas = self.loginHelper.listar_cuentas(self.usuarioActivo)
        if not filas:
            print("No tiene cuentas abiertas.")
            return
        print(tabulate(filas, headers=["Moneda", "Saldo"], tablefmt="grid"))
 
    def menu(self):
        continuar = True
        while continuar:
            print("\n" + 20*"-", "Finanzista MUY Jugete", 20*"-")
            if self.usuarioActivo:
                print(f"  Usuario activo: {self.usuarioActivo}")
            print("1 - Iniciar Sesion")
            print("2 - Crear Usuario")
            print("3 - Abrir Cuenta")
            print("4 - Listar Cuentas")
            print("0 - Salir")
 
            opcion = input().strip()
            match opcion:
                case "1":
                    self.iniciarSesion()
                case "2":
                    self.registrarUsuario()
                case "3":
                    self.abrirCuenta()
                case "4":
                    self.listarCuentas()
                case "0":
                    print("Chau!")
                    continuar = False
                case _:
                    print("Opcion incorrecta")
