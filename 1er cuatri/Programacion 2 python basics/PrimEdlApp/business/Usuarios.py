import bcrypt
import re
import unicodedata
from decimal import Decimal
from data.Usuarios import dataHelper
from business.payments.base import PaymentMethodRegistry
 
 
class LoginHelper:
    def __init__(self):
        self.dh = dataHelper()
 
    # ------------------------------------------------------------------ #
    #  Validaciones de entrada                                             #
    # ------------------------------------------------------------------ #
 
    def sanitize(self, text):
        text = text.strip()
        text = text.lower()
        text = unicodedata.normalize("NFD", text)
        text = text.encode("ascii", "ignore").decode("utf-8")
        text = re.sub(r"[^a-z0-9\-\.]", "", text)
        if len(text) == 0:
            raise ValueError("El nombre de usuario no puede estar vacío o contener solo símbolos")
        return text
 
    def checkEqPwd(self, pwd1, pwd2):
        if pwd1.strip() == pwd2.strip():
            return
        raise ValueError("Las passwords no coinciden")
 
    # ------------------------------------------------------------------ #
    #  Autenticación                                                       #
    # ------------------------------------------------------------------ #
 
    def prepareAndStorePwd(self, username, pwd):
        codedPwd = pwd.encode("utf-8")
        hashedPwd = bcrypt.hashpw(codedPwd, bcrypt.gensalt())
        self.dh.addUser(username, hashedPwd.decode("utf-8"))
 
    def checkUserAndPwd(self, username, pwd):
        hashedpwd = self.dh.getUser(username)
        if hashedpwd is None:
            raise ValueError("Usuario o password inválido")
        if bcrypt.checkpw(pwd.encode("utf-8"), hashedpwd.encode("utf-8")):
            return "OK"
        raise ValueError("Usuario o password inválido")
 
    # ------------------------------------------------------------------ #
    #  Cuentas                                                             #
    # ------------------------------------------------------------------ #
 
    def abrir_cuenta(self, username, moneda):
        if self.dh.getUser(username) is None:
            raise ValueError("Usuario inexistente")
        cuentas = self.dh.getCuentas(username)
        if moneda in cuentas:
            raise ValueError(f"Ya existe una cuenta en {moneda}")
        cuentas[moneda] = Decimal("0")
        self.dh.saveCuentasYTransaccion(
            username, cuentas, {"tipo": "apertura", "moneda": moneda}
        )
 
    def listar_cuentas(self, username):
        cuentas = self.dh.getCuentas(username)
        if not cuentas:
            return []
        return [[moneda, saldo] for moneda, saldo in cuentas.items()]
 
    # ------------------------------------------------------------------ #
    #  Movimientos                                                         #
    # ------------------------------------------------------------------ #
 
    def depositar(self, username, moneda, monto: Decimal):
        """Depósito directo sin pasar por un método de pago (uso interno/tests)."""
        self._validar_monto(monto)
        cuentas = self._obtener_cuenta_existente(username, moneda)
        cuentas[moneda] += monto
        self.dh.saveCuentasYTransaccion(
            username, cuentas,
            {
                "tipo": "deposito",
                "moneda": moneda,
                "monto": str(monto),
                "saldo_resultante": str(cuentas[moneda]),
                "metodo_pago": "directo",
            },
        )
        return cuentas[moneda]
 
    def depositar_con_pago(self, username, moneda, monto: Decimal, metodo_key: str):
        """
        Acredita `monto` en la cuenta sólo si el método de pago aprueba el cobro.
 
        Flujo:
          1. Instancia el método de pago via Registry (factory)
          2. Solicita datos al usuario (interacción en la subclase)
          3. Llama a procesar() — la subclase hace la llamada real al proveedor
          4. Si exitoso → acredita y registra con referencia del proveedor
        """
        self._validar_monto(monto)
        cuentas = self._obtener_cuenta_existente(username, moneda)
 
        # Factory: crea la instancia correcta sin ningún if/elif
        metodo = PaymentMethodRegistry.create(metodo_key)
 
        datos = metodo.solicitar_datos()
        resultado = metodo.procesar(monto, moneda, datos)
 
        if not resultado.get("exitoso"):
            raise ValueError(f"Pago rechazado: {resultado.get('mensaje', 'sin detalle')}")
 
        cuentas[moneda] += monto
        self.dh.saveCuentasYTransaccion(
            username, cuentas,
            {
                "tipo": "deposito",
                "moneda": moneda,
                "monto": str(monto),
                "saldo_resultante": str(cuentas[moneda]),
                "metodo_pago": metodo_key,
                "referencia_pago": resultado.get("referencia", ""),
            },
        )
        return cuentas[moneda], resultado["mensaje"]
 
    def extraer(self, username, moneda, monto: Decimal):
        self._validar_monto(monto)
        cuentas = self._obtener_cuenta_existente(username, moneda)
        if cuentas[moneda] < monto:
            raise ValueError(
                f"Saldo insuficiente en {moneda}: "
                f"disponible {cuentas[moneda]}, requerido {monto}"
            )
        cuentas[moneda] -= monto
        self.dh.saveCuentasYTransaccion(
            username, cuentas,
            {
                "tipo": "extraccion",
                "moneda": moneda,
                "monto": str(monto),
                "saldo_resultante": str(cuentas[moneda]),
            },
        )
        return cuentas[moneda]
 
    def transferir(self, username, moneda_origen, moneda_destino, monto: Decimal, monto_convertido: Decimal):
        self._validar_monto(monto)
        cuentas = self.dh.getCuentas(username)
        for m in (moneda_origen, moneda_destino):
            if m not in cuentas:
                raise ValueError(f"No tenés una cuenta en {m}")
        if cuentas[moneda_origen] < monto:
            raise ValueError(
                f"Saldo insuficiente en {moneda_origen}: "
                f"disponible {cuentas[moneda_origen]}, requerido {monto}"
            )
        cuentas[moneda_origen] -= monto
        cuentas[moneda_destino] += monto_convertido
        self.dh.saveCuentasYTransaccion(
            username, cuentas,
            {
                "tipo": "transferencia",
                "moneda_origen": moneda_origen,
                "monto_origen": str(monto),
                "saldo_origen_resultante": str(cuentas[moneda_origen]),
                "moneda_destino": moneda_destino,
                "monto_destino": str(monto_convertido),
                "saldo_destino_resultante": str(cuentas[moneda_destino]),
            },
        )
        return cuentas[moneda_origen], cuentas[moneda_destino]
 
    # ------------------------------------------------------------------ #
    #  Historial                                                           #
    # ------------------------------------------------------------------ #
 
    def ver_historial(self, username, moneda=None, limite=50):
        return self.dh.getHistorial(username, moneda=moneda, limite=limite)
 
    # ------------------------------------------------------------------ #
    #  Helpers internos                                                    #
    # ------------------------------------------------------------------ #
 
    def _validar_monto(self, monto: Decimal):
        if monto <= Decimal("0"):
            raise ValueError("El monto debe ser mayor a cero")
 
    def _obtener_cuenta_existente(self, username, moneda):
        cuentas = self.dh.getCuentas(username)
        if moneda not in cuentas:
            raise ValueError(f"No tenés una cuenta en {moneda}")
        return cuentas