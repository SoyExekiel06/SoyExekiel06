"""
Contrato abstracto de la capa de datos.
 
Cualquier implementación de persistencia (archivos JSON, SQLObject, etc.)
debe heredar de esta clase e implementar todos sus métodos.
 
La capa de negocio depende únicamente de esta abstracción,
nunca de una implementación concreta.
"""
 
from abc import ABC, abstractmethod
from decimal import Decimal
 
 
class BaseDataHelper(ABC):
 
    # ------------------------------------------------------------------ #
    #  Usuarios                                                            #
    # ------------------------------------------------------------------ #
 
    @abstractmethod
    def addUser(self, username: str, hashedPassword: str) -> None:
        """Crea un nuevo usuario. Lanza ValueError si el nombre ya existe."""
        ...
 
    @abstractmethod
    def getUser(self, username: str) -> str | None:
        """Devuelve el hash de la contraseña, o None si el usuario no existe."""
        ...
 
    # ------------------------------------------------------------------ #
    #  Cuentas                                                             #
    # ------------------------------------------------------------------ #
 
    @abstractmethod
    def getCuentas(self, username: str) -> dict[str, Decimal]:
        """Devuelve {moneda: Decimal} con todos los saldos del usuario."""
        ...
 
    @abstractmethod
    def saveCuentas(self, username: str, cuentas: dict[str, Decimal]) -> None:
        """Actualiza saldos existentes. No crea nuevas cuentas."""
        ...
 
    @abstractmethod
    def saveCuentasYTransaccion(
        self,
        username: str,
        cuentas: dict[str, Decimal],
        transaccion: dict,
    ) -> None:
        """Actualiza saldos Y registra una transacción de forma atómica."""
        ...
 
    # ------------------------------------------------------------------ #
    #  Transacciones                                                       #
    # ------------------------------------------------------------------ #
 
    @abstractmethod
    def appendTransaccion(self, username: str, transaccion: dict) -> None:
        """Agrega una transacción al historial del usuario."""
        ...
 
    @abstractmethod
    def getHistorial(
        self,
        username: str,
        moneda: str | None = None,
        limite: int = 50,
    ) -> list[dict]:
        """
        Devuelve las últimas `limite` transacciones del usuario.
        Opcionalmente filtra por moneda.
        """
