"""
Método de pago: Tarjeta de crédito/débito.
Stub de integración — reemplazar procesar() con Stripe, Decidir, etc.
"""

import uuid
import re
from decimal import Decimal
from datetime import date
from business.payments.base import PaymentMethod, PaymentMethodRegistry


@PaymentMethodRegistry.register("tarjeta")
class TarjetaPayment(PaymentMethod):

    display_name = "Tarjeta de crédito/débito"

    def solicitar_datos(self) -> dict:
        print("  [Tarjeta] Ingresá los datos de tu tarjeta:")

        numero = input("  Número (16 dígitos) > ").strip().replace(" ", "")
        if not re.fullmatch(r"\d{16}", numero):
            raise ValueError("El número de tarjeta debe tener exactamente 16 dígitos")
        if not self._luhn_valido(numero):
            raise ValueError("Número de tarjeta inválido (falló validación Luhn)")

        vencimiento = input("  Vencimiento (MM/AA) > ").strip()
        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", vencimiento):
            raise ValueError("Formato de vencimiento inválido (MM/AA)")
        if not self._no_expirada(vencimiento):
            raise ValueError("La tarjeta está vencida")

        cvv = input("  CVV > ").strip()
        if not re.fullmatch(r"\d{3,4}", cvv):
            raise ValueError("CVV inválido")

        return {
            "numero_enmascarado": f"**** **** **** {numero[-4:]}",
            "vencimiento": vencimiento,
        }

    def procesar(self, monto: Decimal, moneda: str, datos: dict) -> dict:
        referencia = f"TRJ-{uuid.uuid4().hex[:10].upper()}"
        print(f"  [Tarjeta] Procesando cargo de {monto} {moneda} en {datos['numero_enmascarado']}...")
        print(f"  [Tarjeta] ✓ Aprobado — ref: {referencia}")
        return {
            "exitoso": True,
            "referencia": referencia,
            "mensaje": f"Pago aprobado con tarjeta {datos['numero_enmascarado']} (ref: {referencia})",
        }

    @staticmethod
    def _luhn_valido(numero: str) -> bool:
        digitos = [int(d) for d in reversed(numero)]
        total = sum(
            d if i % 2 == 0 else (d * 2 - 9 if d * 2 > 9 else d * 2)
            for i, d in enumerate(digitos)
        )
        return total % 10 == 0

    @staticmethod
    def _no_expirada(vencimiento: str) -> bool:
        mes, anio = vencimiento.split("/")
        exp = date(2000 + int(anio), int(mes), 1)
        hoy = date.today()
        return (exp.year, exp.month) >= (hoy.year, hoy.month)