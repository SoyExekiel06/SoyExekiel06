import json
import os
import requests as req
from decimal import Decimal as dc
import dotenv as de

de.load_dotenv()


class CotizacionHelper:
    """
    Maneja la conexión con la API de Fixer y el caché local de monedas/cotizaciones.
    """

    MONEDAS_FILE = "monedas.json"
    BASE_URL = "https://data.fixer.io/api"

    def __init__(self):
        self.api_key = os.getenv("FIXERio_KEY")
        if not self.api_key:
            raise EnvironmentError(
                "No se encontró API_KEY en el archivo .env"
            )

    # ------------------------------------------------------------------ #
    #  Monedas disponibles                                                 #
    # ------------------------------------------------------------------ #

    def actualizar_monedas(self):
        """
        Descarga la lista de monedas desde Fixer y actualiza monedas.json.
        Devuelve el dict {código: nombre}.
        Lanza excepción si no hay internet Y tampoco existe caché previa.
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

            simbolos = data["symbols"]  # {código: nombre}
            self._guardar_monedas(simbolos)
            return simbolos

        except (req.RequestException, ValueError) as e:
            # Sin internet o API caída → intentar caché
            cache = self._cargar_monedas_cache()
            if cache is None:
                raise ConnectionError(
                    f"No hay conexión y tampoco existe caché local: {e}"
                )
            print(f"[Aviso] Usando caché de monedas ({e})")
            return cache

    def get_monedas(self):
        """
        Devuelve el dict de monedas desde caché.
        Si no existe, intenta descargarlo primero.
        """
        cache = self._cargar_monedas_cache()
        if cache is not None:
            return cache
        # No hay caché → intentar descargar
        return self.actualizar_monedas()

    def moneda_valida(self, codigo):
        """Devuelve True si el código existe en la lista de monedas."""
        monedas = self.get_monedas()
        return codigo.upper() in monedas

    # ------------------------------------------------------------------ #
    #  Cotizaciones                                                        #
    # ------------------------------------------------------------------ #

    def get_tasas(self, base="EUR"):
        """
        Obtiene las tasas de cambio en vivo desde Fixer.
        base: moneda base (solo EUR en plan gratuito).
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

    def convertir(self, monto, moneda_origen, moneda_destino):
        """
        Convierte `monto` de `moneda_origen` a `moneda_destino`.
        Ambas monedas deben ser códigos ISO 4217 válidos.
        Devuelve Decimal con el resultado.
        """
        monto = dc(str(monto))
        moneda_origen = moneda_origen.upper()
        moneda_destino = moneda_destino.upper()

        tasas = self.get_tasas(base="EUR")  # base EUR (plan gratuito)

        # Fixer devuelve tasas respecto a EUR.
        # Para convertir A → B: resultado = monto / tasa_A * tasa_B
        if moneda_origen != "EUR" and moneda_origen not in tasas:
            raise ValueError(f"Moneda origen '{moneda_origen}' no disponible en las tasas")
        if moneda_destino != "EUR" and moneda_destino not in tasas:
            raise ValueError(f"Moneda destino '{moneda_destino}' no disponible en las tasas")

        tasa_origen = dc("1") if moneda_origen == "EUR" else tasas[moneda_origen]
        tasa_destino = dc("1") if moneda_destino == "EUR" else tasas[moneda_destino]

        resultado = monto / tasa_origen * tasa_destino
        return resultado.quantize(dc("0.0001"))

    # ------------------------------------------------------------------ #
    #  Persistencia de caché                                               #
    # ------------------------------------------------------------------ #

    def _guardar_monedas(self, simbolos):
        """Guarda el dict {código: nombre} en monedas.json (sin duplicados)."""
        existentes = self._cargar_monedas_cache() or {}
        existentes.update(simbolos)          # merge: los nuevos sobreescriben
        with open(self.MONEDAS_FILE, "w", encoding="utf-8") as f:
            json.dump(existentes, f, indent=4, ensure_ascii=False)

    def _cargar_monedas_cache(self):
        """Devuelve el dict desde monedas.json, o None si no existe."""
        if not os.path.exists(self.MONEDAS_FILE):
            return None
        with open(self.MONEDAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
        
