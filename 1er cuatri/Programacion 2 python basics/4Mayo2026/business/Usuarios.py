import bcrypt
import re
import unicodedata
from decimal import Decimal
from data.Usuarios import dataHelper
 
class LoginHelper:
    def __init__(self):
        self.dataHelper = dataHelper()
 
    def sanitize(self, text):
        # 1. sacar espacios al inicio y al final
        text = text.strip()
        # 2. pasar a minusculas
        text = text.lower()
        # 3. normalizar unicode y sacar tildes (é -> e, ñ -> n, etc.)
        text = unicodedata.normalize("NFD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")
        # 4. solo permitir letras, numeros, guion y punto
        text = re.sub(r"[^a-z0-9\-\.]", "", text)
        if len(text) == 0:
            raise ValueError("El nombre de usuario no puede estar vacio o contener solo simbolos")
        return text
 
    def checkEqPwd(self, pwd1, pwd2):
        pwd1 = pwd1.strip()
        pwd2 = pwd2.strip()
        if pwd1 == pwd2:
            return
        raise ValueError("Las passwords no coinciden")
 
    def prepareAndStorePwd(self, username, pwd):
        codedPwd = pwd.encode('utf-8')
        hashedPwd = bcrypt.hashpw(codedPwd, bcrypt.gensalt())
        self.dataHelper.addUser(username, hashedPwd.decode('utf-8'))
 
    def checkUserAndPwd(self, username, pwd):
        hashedpwd = self.dataHelper.getUser(username)
        if hashedpwd is None:
            raise ValueError("Usuario o password inválido")
        if bcrypt.checkpw(pwd.encode('utf-8'), hashedpwd.encode('utf-8')):
            return "OK"
        raise ValueError("Usuario o password inválido")
 
    # -- cuentas 
 
    def abrir_cuenta(self, username, moneda):
        # validar que el usuario exista
        if self.dataHelper.getUser(username) is None:
            raise ValueError("Usuario inexistente")
 
        # validar formato de moneda
        moneda = moneda.strip().upper()
        if len(moneda) != 3 or not moneda.isalpha():
            raise ValueError("La moneda debe tener exactamente 3 letras (ISO 4217)")
 
        cuentas = self.dataHelper.getCuentas(username)
 
        # validar que no exista ya
        if moneda in cuentas:
            raise ValueError(f"Ya existe una cuenta en {moneda}")
 
        cuentas[moneda] = Decimal("0")
        self.dataHelper.saveCuentas(username, cuentas)
 
    def listar_cuentas(self, username):
        """Devuelve lista de [moneda, saldo] para tabulate."""
        cuentas = self.dataHelper.getCuentas(username)
        if not cuentas:
            return []
        return [[moneda, saldo] for moneda, saldo in cuentas.items()]