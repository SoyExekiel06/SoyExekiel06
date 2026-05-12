from decimal import Decimal as dc
from data.Cotizacion import CotizacionHelper as ch


class CotizacionService:
    """
    Capa de negocio para cotizaciones y conversiones.
    """

    def __init__(self):
        self.ch = ch()

    def refrescar_monedas(self):
        """Actualiza el caché de monedas y devuelve la cantidad obtenida."""
        monedas = self.ch.actualizar_monedas()
        return len(monedas)

    def listar_monedas(self):
        """
        Devuelve lista de [código, nombre] para tabulate.
        """
        monedas = self.ch.get_monedas()
        return sorted([[k, v] for k, v in monedas.items()])

    def convertir_monto(self, monto_str, origen, destino):
        """
        Valida entradas y delega la conversión al helper.
        Devuelve (monto_origen: Decimal, monto_destino: Decimal).
        """
        try:
            monto = dc(monto_str.replace(",", "."))
        except Exception:
            raise ValueError("El monto ingresado no es un número válido")

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero")

        origen = origen.strip().upper()
        destino = destino.strip().upper()

        if not self.ch.moneda_valida(origen):
            raise ValueError(f"Moneda '{origen}' no reconocida. Consultá las monedas disponibles.")
        if not self.ch.moneda_valida(destino):
            raise ValueError(f"Moneda '{destino}' no reconocida. Consultá las monedas disponibles.")

        resultado = self.ch.convertir(monto, origen, destino)
        return monto, resultado

    def validar_moneda_cuenta(self, codigo):
        """
        Valida que una moneda exista en el listado de Fixer antes de abrir cuenta.
        Lanza ValueError si no es válida.
        """
        codigo = codigo.strip().upper()
        if not self.ch.moneda_valida(codigo):
            raise ValueError(
                f"La moneda '{codigo}' no existe en el listado de Fixer. "
                "Usá '5 - Monedas disponibles' para ver las opciones válidas."
            )
        return codigo