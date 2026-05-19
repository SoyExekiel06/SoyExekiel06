import json
import os
from filelock import FileLock
from decimal import Decimal
from datetime import datetime, timezone
 
 
class dataHelper:
 
    USERS_DIR = "users"
 
    def __init__(self):
        self.usersFile = "users.json"
        self._usersLock = self.usersFile + ".lock"
        os.makedirs(self.USERS_DIR, exist_ok=True)
 
    # ------------------------------------------------------------------ #
    #  Usuarios                                                            #
    # ------------------------------------------------------------------ #
 
    def addUser(self, username, hashedPassword):
        with _lock_file(self._usersLock):
            users = _lock_file._read_json(self, self.usersFile, default={})
            users[username] = hashedPassword
            _lock_file._write_json(self, self.usersFile, users)
 
    def getUser(self, username):
        users = _lock_file._read_json(self, self.usersFile, default={})
        return users.get(username)
 
    # ------------------------------------------------------------------ #
    #  Cuentas (saldos)                                                    #
    # ------------------------------------------------------------------ #
 
    def _cuentasFile(self, username):
        return os.path.join(self.USERS_DIR, f"{username}.json")
 
    def _lockFile(self, username):
        return os.path.join(self.USERS_DIR, f"{username}.lock")
 
    def getCuentas(self, username):
        """Devuelve {moneda: Decimal} desde el archivo del usuario."""
        data = _lock_file._read_json(self, self._cuentasFile(username), default={})
        return {
            moneda: Decimal(saldo)
            for moneda, saldo in data.get("cuentas", {}).items()
        }
 
    def saveCuentas(self, username, cuentas):
        """
        Persiste saldos sin tocar el historial existente.
        Usa file-locking para que 100+ procesos no se pisen.
        """
        with _lock_file(self._lockFile(username)):
            data = _lock_file._read_json(self, self._cuentasFile(username), default={})
            data.setdefault("cuentas", {})
            data["cuentas"] = {m: str(s) for m, s in cuentas.items()}
            _lock_file._write_json(self, self._cuentasFile(username), data)
 
    # ------------------------------------------------------------------ #
    #  Transacciones                                                       #
    # ------------------------------------------------------------------ #
 
    def appendTransaccion(self, username, transaccion: dict):
        """
        Agrega una transacción al historial del usuario de forma atómica.
        transaccion es un dict ya serializable (sin Decimal).
        """
        with _lock_file(self._lockFile(username)):
            data = _lock_file._read_json(self, self._cuentasFile(username), default={})
            data.setdefault("historial", [])
            transaccion["timestamp"] = datetime.now(timezone.utc).isoformat()
            data["historial"].append(transaccion)
            _lock_file._write_json(self, self._cuentasFile(username), data)
 
    def saveCuentasYTransaccion(self, username, cuentas: dict, transaccion: dict):
        """
        Actualiza saldos Y agrega transacción en una sola escritura atómica.
        Usar siempre que un movimiento modifique el saldo.
        """
        with _lock_file(self._lockFile(username)):
            data = _lock_file._read_json(self, self._cuentasFile(username), default={})
            data["cuentas"] = {m: str(s) for m, s in cuentas.items()}
            data.setdefault("historial", [])
            transaccion["timestamp"] = datetime.now(timezone.utc).isoformat()
            data["historial"].append(transaccion)
            _lock_file._write_json(self, self._cuentasFile(username), data)
 
    def getHistorial(self, username, moneda=None, limite=50):
        """
        Devuelve las últimas `limite` transacciones.
        Si se pasa `moneda`, filtra solo las que involucran esa moneda.
        """
        data = _lock_file._read_json(self, self._cuentasFile(username), default={})
        historial = data.get("historial", [])
        if moneda:
            moneda = moneda.upper()
            historial = [
                t for t in historial
                if t.get("moneda") == moneda
                or t.get("moneda_origen") == moneda
                or t.get("moneda_destino") == moneda
            ]
        return historial[-limite:]
 
    # ------------------------------------------------------------------ #
    #  I/O con file-locking (POSIX)                                        #
    # ------------------------------------------------------------------ #
 
    
class _lock_file:
    def __init__(self, path):
        self._lock = FileLock(path)

    def __enter__(self):
        self._lock.acquire()
        return self

    def __exit__(self, *_):
        self._lock.release()
 
    def _read_json(self, path, default=None):
        if not os.path.exists(path):
            return default if default is not None else {}
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
 
    def _write_json(self, path, data):
        # Escritura atómica: escribe en tmp y luego rename
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        os.replace(tmp, path)
