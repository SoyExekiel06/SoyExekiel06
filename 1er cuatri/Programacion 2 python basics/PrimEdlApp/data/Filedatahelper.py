"""
Implementación de persistencia basada en archivos JSON serializados.
 
Estructura de archivos generada:
    data_files/
        users.json          →  { username: hashed_password }
        <username>.json     →  { "cuentas": {moneda: saldo}, "historial": [...] }
 
Cumple exactamente la misma interfaz que dataHelper (SQLObject),
por lo que puede intercambiarse sin tocar las capas de negocio ni presentación.
"""
 
import json
import os
import fcntl
from decimal import Decimal
from datetime import datetime, timezone
 
from .BaseDataHelper import BaseDataHelper
 
# Carpeta donde se guardan todos los archivos. Se crea automáticamente.
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data_files")
 
 
def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)
 
 
def _users_path() -> str:
    return os.path.join(DATA_DIR, "users.json")
 
 
def _user_path(username: str) -> str:
    return os.path.join(DATA_DIR, f"{username}.json")
 
 
# ------------------------------------------------------------------ #
#  Helpers de lectura/escritura con file-locking                      #
# ------------------------------------------------------------------ #
 
def _read_json(path: str, default):
    """Lee un JSON; devuelve `default` si el archivo no existe."""
    if not os.path.exists(path):
        return default
    with open(path, "r", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        try:
            return json.load(f)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
 
 
def _write_json(path: str, data) -> None:
    """Escribe `data` como JSON con lock exclusivo."""
    _ensure_dir()
    with open(path, "w", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)
 
 
# ------------------------------------------------------------------ #
#  Helpers de conversión Decimal ↔ str (para JSON)                   #
# ------------------------------------------------------------------ #
 
def _cuentas_to_json(cuentas: dict[str, Decimal]) -> dict:
    return {k: str(v) for k, v in cuentas.items()}
 
 
def _cuentas_from_json(raw: dict) -> dict[str, Decimal]:
    return {k: Decimal(v) for k, v in raw.items()}
 
 
# ------------------------------------------------------------------ #
#  Implementación                                                     #
# ------------------------------------------------------------------ #
 
class FileDataHelper(BaseDataHelper):
    """
    Persiste todos los datos en archivos JSON dentro de data_files/.
    Ofrece exactamente la misma interfaz pública que dataHelper (SQLObject).
    """
 
    def __init__(self):
        _ensure_dir()
 
    # ------------------------------------------------------------------ #
    #  Usuarios                                                            #
    # ------------------------------------------------------------------ #
 
    def addUser(self, username: str, hashedPassword: str) -> None:
        """Crea un nuevo usuario. Lanza ValueError si ya existe."""
        users = _read_json(_users_path(), {})
        if username in users:
            raise ValueError(f"El usuario '{username}' ya existe")
        users[username] = hashedPassword
        _write_json(_users_path(), users)
 
        # Crear archivo de usuario vacío
        _write_json(_user_path(username), {"cuentas": {}, "historial": []})
 
    def getUser(self, username: str) -> str | None:
        """Devuelve el hash de la contraseña, o None si no existe."""
        users = _read_json(_users_path(), {})
        return users.get(username)
 
    # ------------------------------------------------------------------ #
    #  Cuentas                                                             #
    # ------------------------------------------------------------------ #
 
    def getCuentas(self, username: str) -> dict[str, Decimal]:
        """Devuelve {moneda: Decimal} con todos los saldos del usuario."""
        data = _read_json(_user_path(username), {"cuentas": {}, "historial": []})
        return _cuentas_from_json(data.get("cuentas", {}))
 
    def saveCuentas(self, username: str, cuentas: dict[str, Decimal]) -> None:
        """Actualiza saldos. No registra transacción."""
        path = _user_path(username)
        data = _read_json(path, {"cuentas": {}, "historial": []})
        data["cuentas"] = _cuentas_to_json(cuentas)
        _write_json(path, data)
 
    def saveCuentasYTransaccion(
        self,
        username: str,
        cuentas: dict[str, Decimal],
        transaccion: dict,
    ) -> None:
        """Actualiza saldos y registra la transacción en una sola escritura."""
        path = _user_path(username)
        data = _read_json(path, {"cuentas": {}, "historial": []})
        data["cuentas"] = _cuentas_to_json(cuentas)
        data["historial"].append(self._enriquecer_transaccion(transaccion))
        _write_json(path, data)
 
    # ------------------------------------------------------------------ #
    #  Transacciones                                                       #
    # ------------------------------------------------------------------ #
 
    def appendTransaccion(self, username: str, transaccion: dict) -> None:
        """Agrega una transacción al historial. Si es apertura, crea la cuenta."""
        path = _user_path(username)
        data = _read_json(path, {"cuentas": {}, "historial": []})
 
        if transaccion.get("tipo") == "apertura":
            moneda = transaccion["moneda"]
            if moneda not in data["cuentas"]:
                data["cuentas"][moneda] = "0"
 
        data["historial"].append(self._enriquecer_transaccion(transaccion))
        _write_json(path, data)
 
    def getHistorial(
        self,
        username: str,
        moneda: str | None = None,
        limite: int = 50,
    ) -> list[dict]:
        """Devuelve las últimas `limite` transacciones, con filtro opcional de moneda."""
        data = _read_json(_user_path(username), {"cuentas": {}, "historial": []})
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
    #  Helper interno                                                      #
    # ------------------------------------------------------------------ #
 
    @staticmethod
    def _enriquecer_transaccion(transaccion: dict) -> dict:
        """Agrega timestamp si no viene incluido."""
        t = dict(transaccion)
        if "timestamp" not in t:
            t["timestamp"] = datetime.now(timezone.utc).isoformat()
        return t
