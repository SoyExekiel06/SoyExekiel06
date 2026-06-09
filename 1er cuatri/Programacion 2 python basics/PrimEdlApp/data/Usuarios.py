from decimal import Decimal
from datetime import datetime, timezone
from sqlobject import SQLObjectNotFound
 
from .Models import Usuario, Cuenta, Transaccion
 

 
class dataHelper:
 
    # ------------------------------------------------------------------ #
    #  Usuarios                                                            #
    # ------------------------------------------------------------------ #
 
    def addUser(self, username: str, hashedPassword: str) -> None:
        """Crea un nuevo usuario. Lanza ValueError si el nombre ya existe."""
        try:
            Usuario.byUsername(username)
            raise ValueError(f"El usuario '{username}' ya existe")
        except SQLObjectNotFound:
            pass
        Usuario(username=username, hashed_password=hashedPassword)
 
    def getUser(self, username: str) -> str | None:
        """Devuelve el hash de la contraseña, o None si el usuario no existe."""
        try:
            return Usuario.byUsername(username).hashed_password
        except SQLObjectNotFound:
            return None
 
    def _get_usuario_obj(self, username: str) -> Usuario:
        """Devuelve el objeto Usuario o lanza SQLObjectNotFound."""
        return Usuario.byUsername(username)
 
    # ------------------------------------------------------------------ #
    #  Cuentas (saldos)                                                    #
    # ------------------------------------------------------------------ #
 
    def getCuentas(self, username: str) -> dict[str, Decimal]:
        """Devuelve {moneda: Decimal} con todos los saldos del usuario."""
        try:
            usuario = self._get_usuario_obj(username)
        except SQLObjectNotFound:
            return {}
        # ForeignKey genera columna usuarioID → usar usuarioID= en selectBy
        return {
            c.moneda: Decimal(str(c.saldo))
            for c in Cuenta.selectBy(usuarioID=usuario.id)
        }
 
    def saveCuentas(self, username: str, cuentas: dict[str, Decimal]) -> None:
        """Actualiza saldos existentes. No crea nuevas cuentas."""
        usuario = self._get_usuario_obj(username)
        for moneda, saldo in cuentas.items():
            resultados = list(Cuenta.selectBy(usuarioID=usuario.id, moneda=moneda))
            if resultados:
                resultados[0].saldo = saldo
 
    def saveCuentasYTransaccion(
        self,
        username: str,
        cuentas: dict[str, Decimal],
        transaccion: dict,
    ) -> None:
        """
        Actualiza saldos Y agrega transacción.
        Reemplaza la escritura atómica con file-locking del original.
        """
        usuario = self._get_usuario_obj(username)
 
        for moneda, saldo in cuentas.items():
            resultados = list(Cuenta.selectBy(usuarioID=usuario.id, moneda=moneda))
            if resultados:
                resultados[0].saldo = saldo
            else:
                # usuarioID= para pasar la FK como entero; SQLObject lo acepta también
                # como objeto, pero con ForeignKey el keyword debe ser usuarioID
                Cuenta(usuarioID=usuario.id, moneda=moneda, saldo=saldo)
 
        self._crear_transaccion(usuario, transaccion)
 
    # ------------------------------------------------------------------ #
    #  Transacciones                                                       #
    # ------------------------------------------------------------------ #
 
    def appendTransaccion(self, username: str, transaccion: dict) -> None:
        """
        Agrega una transacción al historial.
        Para apertura de cuenta también crea la fila en Cuenta.
        """
        usuario = self._get_usuario_obj(username)
 
        if transaccion.get("tipo") == "apertura":
            moneda = transaccion["moneda"]
            existe = list(Cuenta.selectBy(usuarioID=usuario.id, moneda=moneda))
            if not existe:
                Cuenta(usuarioID=usuario.id, moneda=moneda, saldo=Decimal("0"))
 
        self._crear_transaccion(usuario, transaccion)
 
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
        try:
            usuario = self._get_usuario_obj(username)
        except SQLObjectNotFound:
            return []
 
        registros = list(
            Transaccion.selectBy(usuarioID=usuario.id).orderBy("timestamp")
        )
 
        if moneda:
            moneda = moneda.upper()
            registros = [
                r for r in registros
                if r.moneda == moneda
                or r.moneda_origen == moneda
                or r.moneda_destino == moneda
            ]
 
        return [self._transaccion_a_dict(r) for r in registros[-limite:]]
 
    # ------------------------------------------------------------------ #
    #  Helpers internos                                                    #
    # ------------------------------------------------------------------ #
 
    def _crear_transaccion(self, usuario: Usuario, data: dict) -> None:
        """Inserta una fila en transaccion a partir de un dict."""
        ts = datetime.now(timezone.utc).replace(tzinfo=None)
 
        def _dec(key: str) -> Decimal | None:
            val = data.get(key)
            return Decimal(str(val)) if val is not None else None
 
        Transaccion(
            usuarioID=usuario.id,
            tipo=data.get("tipo", ""),
            timestamp=ts,
            moneda=data.get("moneda"),
            monto=_dec("monto"),
            saldo_resultante=_dec("saldo_resultante"),
            moneda_origen=data.get("moneda_origen"),
            monto_origen=_dec("monto_origen"),
            saldo_origen_resultante=_dec("saldo_origen_resultante"),
            moneda_destino=data.get("moneda_destino"),
            monto_destino=_dec("monto_destino"),
            saldo_destino_resultante=_dec("saldo_destino_resultante"),
            metodo_pago=data.get("metodo_pago"),
            referencia_pago=data.get("referencia_pago"),
        )
 
    @staticmethod
    def _transaccion_a_dict(t: Transaccion) -> dict:
        """Convierte objeto Transaccion al dict que usa la capa de negocio."""
        d: dict = {
            "tipo": t.tipo,
            "timestamp": t.timestamp.isoformat() + "Z",
        }
        if t.moneda:
            d["moneda"] = t.moneda
        if t.monto is not None:
            d["monto"] = str(t.monto)
        if t.saldo_resultante is not None:
            d["saldo_resultante"] = str(t.saldo_resultante)
        if t.moneda_origen:
            d["moneda_origen"] = t.moneda_origen
        if t.monto_origen is not None:
            d["monto_origen"] = str(t.monto_origen)
        if t.saldo_origen_resultante is not None:
            d["saldo_origen_resultante"] = str(t.saldo_origen_resultante)
        if t.moneda_destino:
            d["moneda_destino"] = t.moneda_destino
        if t.monto_destino is not None:
            d["monto_destino"] = str(t.monto_destino)
        if t.saldo_destino_resultante is not None:
            d["saldo_destino_resultante"] = str(t.saldo_destino_resultante)
        if t.metodo_pago:
            d["metodo_pago"] = t.metodo_pago
        if t.referencia_pago:
            d["referencia_pago"] = t.referencia_pago
        return d