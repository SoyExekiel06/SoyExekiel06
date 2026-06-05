import getpass
from decimal import Decimal, InvalidOperation
from tabulate import tabulate
from business.Usuarios import LoginHelper
from business.Cotizacion import CotizacionService
 
 
class App:
    def __init__(self):
        self.usuarioActivo = None
        self.lh = LoginHelper()
        self.cs = CotizacionService()
 
    # ------------------------------------------------------------------ #
    #  Helpers de input                                                    #
    # ------------------------------------------------------------------ #
 
    def _input_monto(self, prompt) -> Decimal:
        raw = input(prompt).strip().replace(",", ".")
        try:
            monto = Decimal(raw)
        except InvalidOperation:
            raise ValueError("El monto ingresado no es un número válido")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")
        return monto
 
    def _input_moneda(self, prompt) -> str:
        return input(prompt).strip().upper()
 
    # ------------------------------------------------------------------ #
    #  Autenticación                                                       #
    # ------------------------------------------------------------------ #
 
    def registrarUsuario(self):
        try:
            username = input("Ingrese el nuevo nombre de usuario:\n> ")
            username = self.lh.sanitize(username)
            pwd1 = getpass.getpass(prompt="Ingrese su password:\n> ")
            pwd2 = getpass.getpass(prompt="Repita la password:\n> ")
            self.lh.checkEqPwd(pwd1, pwd2)
            self.lh.prepareAndStorePwd(username, pwd1)
            print(f"  Usuario '{username}' creado correctamente.")
        except Exception as e:
            print(f"  Error: {e}")
 
    def iniciarSesion(self):
        try:
            username = input("Ingrese el nombre de usuario:\n> ")
            username = self.lh.sanitize(username)
            pwd = getpass.getpass(prompt="Ingrese su password:\n> ")
            self.lh.checkUserAndPwd(username, pwd)
            self.usuarioActivo = username
            print(f"  Bienvenido, {username}!")
        except ValueError as e:
            print(f"  Error: {e}")
 
    # ------------------------------------------------------------------ #
    #  Cuentas                                                             #
    # ------------------------------------------------------------------ #
 
    def abrirCuenta(self):
        if not self.usuarioActivo:
            print("  Debe iniciar sesión primero.")
            return
        try:
            moneda = self._input_moneda("Ingrese el código de moneda (ej: USD, ARS, EUR):\n> ")
            moneda = self.cs.validar_moneda_cuenta(moneda)
            self.lh.abrir_cuenta(self.usuarioActivo, moneda)
            print(f"  Cuenta en {moneda} abierta correctamente.")
        except (ValueError, ConnectionError) as e:
            print(f"  Error: {e}")
 
    def listarCuentas(self):
        if not self.usuarioActivo:
            print("  Debe iniciar sesión primero.")
            return
        filas = self.lh.listar_cuentas(self.usuarioActivo)
        if not filas:
            print("  No tiene cuentas abiertas.")
            return
        print(tabulate(filas, headers=["Moneda", "Saldo"], tablefmt="grid"))
 
    # ------------------------------------------------------------------ #
    #  Movimientos                                                         #
    # ------------------------------------------------------------------ #
 
    def depositar(self):
        if not self.usuarioActivo:
            print("  Debe iniciar sesión primero.")
            return
        try:
            moneda = self._input_moneda("Moneda de la cuenta:\n> ")
            monto = self._input_monto(f"Monto a depositar en {moneda}:\n> ")
            saldo = self.lh.depositar(self.usuarioActivo, moneda, monto)
            print(f"  Depósito registrado. Nuevo saldo en {moneda}: {saldo}")
        except (ValueError, ConnectionError) as e:
            print(f"  Error: {e}")
 
    def extraer(self):
        if not self.usuarioActivo:
            print("  Debe iniciar sesión primero.")
            return
        try:
            moneda = self._input_moneda("Moneda de la cuenta:\n> ")
            monto = self._input_monto(f"Monto a extraer de {moneda}:\n> ")
            saldo = self.lh.extraer(self.usuarioActivo, moneda, monto)
            print(f"  Extracción registrada. Nuevo saldo en {moneda}: {saldo}")
        except ValueError as e:
            print(f"  Error: {e}")
 
    def transferir(self):
        """Convierte y mueve fondos entre dos cuentas del mismo usuario."""
        if not self.usuarioActivo:
            print("  Debe iniciar sesión primero.")
            return
        try:
            origen = self._input_moneda("Moneda de origen:\n> ")
            destino = self._input_moneda("Moneda de destino:\n> ")
            monto = self._input_monto(f"Monto a transferir en {origen}:\n> ")
 
            # Cotizar antes de tocar saldos
            _, monto_convertido = self.cs.convertir_monto(str(monto), origen, destino)
 
            print(f"\n  Se acreditarán {monto_convertido} {destino} (cotización actual).")
            confirmar = input("  ¿Confirmar transferencia? (s/n): ").strip().lower()
            if confirmar != "s":
                print("  Transferencia cancelada.")
                return
 
            saldo_origen, saldo_destino = self.lh.transferir(
                self.usuarioActivo, origen, destino, monto, monto_convertido
            )
            print(f"  Transferencia realizada.")
            print(f"  Saldo {origen}: {saldo_origen}")
            print(f"  Saldo {destino}: {saldo_destino}")
 
        except (ValueError, ConnectionError) as e:
            print(f"  Error: {e}")
 
    # ------------------------------------------------------------------ #
    #  Historial                                                           #
    # ------------------------------------------------------------------ #
 
    def verHistorial(self):
        if not self.usuarioActivo:
            print("  Debe iniciar sesión primero.")
            return
        try:
            moneda_input = input(
                "Filtrar por moneda (dejar vacío para ver todo):\n> "
            ).strip().upper() or None
 
            limite_input = input("Cantidad de movimientos a mostrar (vacío = 50):\n> ").strip()
            limite = int(limite_input) if limite_input.isdigit() else 50
 
            historial = self.lh.ver_historial(
                self.usuarioActivo, moneda=moneda_input, limite=limite
            )
 
            if not historial:
                print("  No hay movimientos registrados.")
                return
 
            filas = []
            for t in historial:
                tipo = t.get("tipo", "?")
                ts = t.get("timestamp", "")[:19].replace("T", " ")  # legible
 
                if tipo == "apertura":
                    filas.append([ts, tipo, t.get("moneda", ""), "", ""])
 
                elif tipo in ("deposito", "extraccion"):
                    filas.append([
                        ts, tipo,
                        t.get("moneda", ""),
                        t.get("monto", ""),
                        t.get("saldo_resultante", ""),
                    ])
 
                elif tipo == "transferencia":
                    filas.append([
                        ts, tipo,
                        f"{t.get('moneda_origen')} → {t.get('moneda_destino')}",
                        f"-{t.get('monto_origen')} / +{t.get('monto_destino')}",
                        f"{t.get('saldo_origen_resultante')} / {t.get('saldo_destino_resultante')}",
                    ])
 
            print(tabulate(
                filas,
                headers=["Fecha/Hora", "Tipo", "Moneda(s)", "Monto", "Saldo resultante"],
                tablefmt="grid",
            ))
 
        except Exception as e:
            print(f"  Error: {e}")
 
    # ------------------------------------------------------------------ #
    #  Cotizaciones                                                        #
    # ------------------------------------------------------------------ #
 
    def convertirMonto(self):
        try:
            origen = self._input_moneda("Moneda de origen (ej: USD):\n> ")
            destino = self._input_moneda("Moneda de destino (ej: ARS):\n> ")
            monto_str = input(f"Monto en {origen}:\n> ").strip()
 
            monto, resultado = self.cs.convertir_monto(monto_str, origen, destino)
            print(f"\n  {monto} {origen}  →  {resultado} {destino}")
        except (ValueError, ConnectionError) as e:
            print(f"  Error: {e}")
 
    def mostrarMonedasDisponibles(self):
        try:
            filas = self.cs.listar_monedas()
            if not filas:
                print("  No hay monedas en caché. Intentando descargar...")
                n = self.cs.refrescar_monedas()
                filas = self.cs.listar_monedas()
                print(f"  Se descargaron {n} monedas.\n")
            print(tabulate(filas, headers=["Código", "Nombre"], tablefmt="grid"))
        except (ConnectionError, EnvironmentError) as e:
            print(f"  Error: {e}")
 
    def refrescarMonedas(self):
        try:
            n = self.cs.refrescar_monedas()
            print(f"  Caché actualizado: {n} monedas descargadas.")
        except (ConnectionError, EnvironmentError) as e:
            print(f"  Error: {e}")

    def depositar_con_pago(self):
        """Ingresa fondos a una cuenta usando un método de pago externo."""
        if not self.usuarioActivo:
            print("  Debe iniciar sesión primero.")
            return
        try:
            # 1. Elegir cuenta destino
            moneda = self._input_moneda("Moneda de la cuenta a acreditar (ej: ARS):\n> ")
            self.cs.validar_moneda_cuenta(moneda)

            # 2. Monto
            monto = self._input_monto(f"Monto a ingresar en {moneda}:\n> ")

            # 3. Mostrar métodos disponibles dinámicamente
            from business.payments import PaymentMethodRegistry
            disponibles = PaymentMethodRegistry.disponibles()
            if not disponibles:
                print("  No hay métodos de pago disponibles.")
                return

            print("\n  Métodos de pago disponibles:")
            for i, (clave, nombre) in enumerate(disponibles, 1):
                print(f"  {i} - {nombre}")
            print("  0 - Cancelar")

            opcion = input("> ").strip()
            if opcion == "0":
                print("  Operación cancelada.")
                return
            if not opcion.isdigit() or not (1 <= int(opcion) <= len(disponibles)):
                print("  Opción inválida.")
                return

            clave, nombre = disponibles[int(opcion) - 1]

            # 4. Solicitar datos y procesar
            metodo = PaymentMethodRegistry.create(clave)
            datos = metodo.solicitar_datos()
            resultado = metodo.procesar(monto, moneda, datos)

            if not resultado.get("exitoso"):
                print(f"  Pago rechazado: {resultado.get('mensaje', 'sin detalle')}")
                return

            # 5. Acreditar en la cuenta
            saldo = self.lh.depositar(self.usuarioActivo, moneda, monto)
            print(f"\n  ✓ {resultado['mensaje']}")
            print(f"  Nuevo saldo en {moneda}: {saldo}")

        except (ValueError, ConnectionError) as e:
            print(f"  Error: {e}")

    def egresar_con_pago(self):
        """Retira fondos de una cuenta enviándolos a un método de pago externo."""
        if not self.usuarioActivo:
            print("  Debe iniciar sesión primero.")
            return
        try:
            moneda = self._input_moneda("Moneda de la cuenta a debitar (ej: ARS):\n> ")
            monto = self._input_monto(f"Monto a retirar en {moneda}:\n> ")

            from business.payments import PaymentMethodRegistry
            disponibles = [
            (clave, nombre)
            for clave, nombre in PaymentMethodRegistry.disponibles()
            if self._metodo_soporta_egreso(clave)
            ]

            if not disponibles:
                print("  No hay métodos de pago que soporten egresos.")
                return

            print("\n  Métodos disponibles para retiro:")
            for i, (clave, nombre) in enumerate(disponibles, 1):
                print(f"  {i} - {nombre}")
            print("  0 - Cancelar")

            opcion = input("> ").strip()
            if opcion == "0":
                print("  Operación cancelada.")
                return
            if not opcion.isdigit() or not (1 <= int(opcion) <= len(disponibles)):
                print("  Opción inválida.")
                return

            clave, nombre = disponibles[int(opcion) - 1]
            metodo = PaymentMethodRegistry.create(clave)
            datos = metodo.solicitar_datos()

            # Primero descontar saldo, luego intentar envío
            saldo = self.lh.extraer(self.usuarioActivo, moneda, monto)
            resultado = metodo.acreditar(monto, moneda, datos)

            if not resultado.get("exitoso"):
                # Revertir la extracción si el envío falló
                self.lh.depositar(self.usuarioActivo, moneda, monto)
                print(f"  Retiro fallido: {resultado.get('mensaje', 'sin detalle')}")
                return

            print(f"\n  ✓ {resultado['mensaje']}")
            print(f"  Nuevo saldo en {moneda}: {saldo}")

        except (ValueError, ConnectionError, NotImplementedError) as e:
            print(f"  Error: {e}")

    def _metodo_soporta_egreso(self, clave: str) -> bool:
        """Devuelve True si el método implementa acreditar() correctamente."""
        try:
            metodo = self.PaymentMethodRegistry.create(clave)
            # Intenta con valores dummy para ver si lanza NotImplementedError
            from decimal import Decimal
            metodo.acreditar(Decimal("0"), "", {})
            return True
        except NotImplementedError:
            return False
        except Exception:
            return True
 
    # ------------------------------------------------------------------ #
    #  Menú de acceso                                                      #
    # ------------------------------------------------------------------ #
 
    def menu_acceso(self):
        while True:
            print("\n" + "=" * 55)
            print("         Finanzista MUY Juguete  ")
            print("=" * 55)
            print("  1 - Iniciar sesión")
            print("  2 - Crear usuario")
            print("  0 - Salir")
            print("-" * 55)
 
            match input("> ").strip():
                case "1":
                    self.iniciarSesion()
                    if self.usuarioActivo:
                        self.menu_principal()
                case "2":
                    self.registrarUsuario()
                case "0":
                    print("  ¡Hasta luego!")
                    break
                case _:
                    print("  Opción incorrecta.")
 
    # ------------------------------------------------------------------ #
    #  Menú principal                                                      #
    # ------------------------------------------------------------------ #
    
    def menu_principal(self):
        while self.usuarioActivo:
            print("\n" + "=" * 55)
            print(f"  {self.usuarioActivo}")
            print("=" * 55)
            print("  --- Cuentas ---")
            print("  1 - Abrir cuenta")
            print("  2 - Listar mis cuentas")
            print("  --- Movimientos ---")
            print("  3 - Depositar")
            print("  4 - Extraer")
            print("  5 - Transferir entre cuentas (con conversión)")
            print("  6 - Ver historial")
            print("  7 - Ingresar fondos (Mercado Pago / Tarjeta)")
            print("  8 - Retirar fondos (Mercado Pago)")
            print("  --- Cotizaciones ---")
            print("  9 - Convertir monto entre monedas")
            print("  10 - Ver monedas disponibles")
            print("  11 - Actualizar lista de monedas (online)")
            print("  --- Sesión ---")
            print("  0 - Cerrar sesión")
            print("-" * 55)

            match input("> ").strip():
                case "1":
                    self.abrirCuenta()
                case "2":
                    self.listarCuentas()
                case "3":
                    self.depositar()
                case "4":
                    self.extraer()
                case "5":
                    self.transferir()
                case "6":
                    self.verHistorial()
                case "7":
                    self.depositar_con_pago()
                case "8":
                    self.egresar_con_pago()
                case "9":
                    self.convertirMonto()
                case "10":
                    self.mostrarMonedasDisponibles()
                case "11":
                    self.refrescarMonedas()
                case "0":
                    print(f"  Sesión de '{self.usuarioActivo}' cerrada.")
                    self.usuarioActivo = None
                case _:
                    print("  Opción incorrecta.")
