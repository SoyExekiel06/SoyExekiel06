import json
import os
from decimal import Decimal
 
class dataHelper:
 
    USERS_DIR = "users"
 
    def __init__(self):
        self.usersFile = 'users.json'
        os.makedirs(self.USERS_DIR, exist_ok=True)  # crea la carpeta si no existe
 
    # -- usuarios 
 
    def addUser(self, username, hashedPassword):
        users = self.deserialize(self.usersFile)
        users[username] = hashedPassword
        self.serialize(users, self.usersFile)
 
    def getUser(self, username):
        users = self.deserialize(self.usersFile)
        try:
            return users[username]
        except KeyError:
            return None
 
    # -- cuentas 
 
    def _cuentasFile(self, username):
        return os.path.join(self.USERS_DIR, f"{username}.json")
 
    def getCuentas(self, username):
        """Devuelve el dict de cuentas del usuario. Si no existe el archivo, devuelve {}."""
        file = self._cuentasFile(username)
        if not os.path.exists(file):
            return {}
        with open(file, "r") as f:
            raw = json.loads(f.read())
        # convertir valores a Decimal al deserializar
        return {moneda: Decimal(saldo) for moneda, saldo in raw.items()}
 
    def saveCuentas(self, username, cuentas):
        """Persiste el dict de cuentas (valores Decimal) como strings en JSON."""
        file = self._cuentasFile(username)
        serializable = {moneda: str(saldo) for moneda, saldo in cuentas.items()}
        with open(file, "w") as f:
            f.write(json.dumps(serializable, indent=4))
 
    # -- helpers genéricos 
 
    def serialize(self, data, file):
        with open(file, "w") as f:
            f.write(json.dumps(data, indent=4))
 
    def deserialize(self, file):
        with open(file, "r") as f:
            return json.loads(f.read())