import os
import requests as req
from decimal import Decimal as dc
from datetime import datetime
from sqlobject import SQLObjectNotFound
import dotenv as de
from data import Models as m
 
de.load_dotenv()
 
 
class CotizacionHelper:
    """
    Maneja la conexión con la API de Fixer y el caché de monedas en la BD.
    """

    BASE_URL = "http://data.fixer.io/api"
 
    def __init__(self):
        self.api_key = os.getenv("FIXERio_KEY")
        if not self.api_key:
            raise EnvironmentError("No se encontró FIXERio_KEY en el archivo .env")
 
    # ------------------------------------------------------------------ #
    #  Monedas disponibles                                                 #
    # ------------------------------------------------------------------ #
 
    def actualizar_monedas(self) -> dict[str, str]:
        """
        Descarga la lista de monedas desde Fixer y actualiza la tabla `moneda`.
        Devuelve el dict {código: nombre}.
        Lanza excepción si no hay internet Y tampoco existe caché en BD.
        """
        try:
            response = req.get(
                f"{self.BASE_URL}/symbols",
                params={"access_key": self.api_key},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
 
            if not data.get("success"):
                raise ValueError(
                    f"Error de la API Fixer: {data.get('error', {}).get('info', 'desconocido')}"
                )
 
            simbolos = data["symbols"]
            self._guardar_monedas(simbolos)
            return simbolos
 
        except (req.RequestException, ValueError) as e:
            cache = self._cargar_monedas_cache()
            if not cache:
                raise ConnectionError(
                    f"No hay conexión y tampoco existe caché local: {e}"
                )
            print(f"[Aviso] Usando caché de monedas ({e})")
            return cache
 
    def get_monedas(self) -> dict[str, str]:
        """
        Devuelve el dict de monedas desde caché en BD.
        Si no existe, intenta descargarlo primero.
        """
        cache = self._cargar_monedas_cache()
        if cache:
            return cache
        return self.actualizar_monedas()
 
    def moneda_valida(self, codigo: str) -> bool:
        """Devuelve True si el código existe en la tabla moneda."""
        monedas = self.get_monedas()
        return codigo.upper() in monedas
 
    # ------------------------------------------------------------------ #
    #  Cotizaciones                                                        #
    # ------------------------------------------------------------------ #
 
    def get_tasas(self, base: str = "EUR") -> dict[str, dc]:
        """
        Obtiene las tasas de cambio en vivo desde Fixer.
        Devuelve dict {código: Decimal(tasa)}.
        """
        try:
            response = req.get(
                f"{self.BASE_URL}/latest",
                params={"access_key": self.api_key, "base": base},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
 
            if not data.get("success"):
                raise ValueError(
                    f"Error de la API Fixer: {data.get('error', {}).get('info', 'desconocido')}"
                )
 
            return {k: dc(str(v)) for k, v in data["rates"].items()}
 
        except req.RequestException as e:
            raise ConnectionError(f"No se pudo obtener cotizaciones: {e}")
 
    def convertir(self, monto: dc, moneda_origen: str, moneda_destino: str) -> dc:
        """
        Convierte `monto` de `moneda_origen` a `moneda_destino`.
        Devuelve Decimal con el resultado.
        """
        monto = dc(str(monto))
        moneda_origen = moneda_origen.upper()
        moneda_destino = moneda_destino.upper()
 
        tasas = self.get_tasas(base="EUR")
 
        if moneda_origen != "EUR" and moneda_origen not in tasas:
            raise ValueError(f"Moneda origen '{moneda_origen}' no disponible en las tasas")
        if moneda_destino != "EUR" and moneda_destino not in tasas:
            raise ValueError(f"Moneda destino '{moneda_destino}' no disponible en las tasas")
 
        tasa_origen = dc("1") if moneda_origen == "EUR" else tasas[moneda_origen]
        tasa_destino = dc("1") if moneda_destino == "EUR" else tasas[moneda_destino]
 
        resultado = monto / tasa_origen * tasa_destino
        return resultado.quantize(dc("0.01"))
 
    # ------------------------------------------------------------------ #
    #  Persistencia de caché en MySQL (reemplaza monedas.json)            #
    # ------------------------------------------------------------------ #
 
    def _guardar_monedas(self, simbolos: dict[str, str]) -> None:
        """
        Hace un UPSERT de cada moneda en la tabla `moneda`.
        Equivalente a json.dump en el original pero con SQL.
        """
        now = datetime.utcnow()
        for codigo, nombre in simbolos.items():
            codigo = codigo.upper()
            try:
                moneda = m.Moneda.byCodigo(codigo)
                moneda.nombre = nombre
                moneda.updated_at = now
            except SQLObjectNotFound:
                m.Moneda(codigo=codigo, nombre=nombre, updated_at=now)
 
    def _cargar_monedas_cache(self) -> dict[str, str] | None:
        """
        Devuelve {código: nombre} desde la tabla moneda.
        Devuelve None si la tabla está vacía.
        Equivalente a json.load en el original.
        """
        registros = list(m.Moneda.select())
        if not registros:
            return None
        return {m.codigo: m.nombre for m in registros}
