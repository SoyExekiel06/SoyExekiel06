"""
Método de pago: Mercado Pago.
Stub de integración — reemplazar procesar() con el SDK real cuando corresponda.
"""
 
import uuid
from decimal import Decimal
from business.payments.base import PaymentMethod, PaymentMethodRegistry
 
 
@PaymentMethodRegistry.register("mercadopago")
class MercadoPagoPayment(PaymentMethod):
 
    display_name = "Mercado Pago"
 
    def solicitar_datos(self) -> dict:
        print("  [Mercado Pago] Ingresá tu CVU o alias:")
        cvu = input("  CVU/Alias > ").strip()
        if not cvu:
            raise ValueError("El CVU/alias no puede estar vacío")
        return {"cvu": cvu}
 
    def procesar(self, monto: Decimal, moneda: str, datos: dict) -> dict:
        """
        Aquí iría la llamada real al SDK de Mercado Pago.
        Por ahora simula una aprobación instantánea.
        """
        # --- integración real (ejemplo) ---
        # import mercadopago
        # sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))
        # result = sdk.payment().create({...})
        # aprobado = result["response"]["status"] == "approved"
        # ---------------------------------
 
        referencia = f"MP-{uuid.uuid4().hex[:10].upper()}"
        print(f"  [Mercado Pago] Procesando pago de {monto} {moneda}...")
        print(f"  [Mercado Pago] ✓ Aprobado — ref: {referencia}")
 
        return {
            "exitoso": True,
            "referencia": referencia,
            "mensaje": f"Pago aprobado por Mercado Pago (ref: {referencia})",
        }
    def acreditar(self, monto: Decimal, moneda: str, datos: dict) -> dict:
        """
        Envía fondos al CVU/alias del usuario.
         Stub — reemplazar con SDK real.
        """
        # --- integración real ---
        # sdk = mercadopago.SDK(os.getenv("MP_ACCESS_TOKEN"))
        # result = sdk.payment().create({
        #     "transaction_amount": float(monto),
        #     "payment_method_id": "account_money",
        #     "receiver": {"alias": datos["cvu"]},
        # })
        # -----------------------

        referencia = f"MP-OUT-{uuid.uuid4().hex[:10].upper()}"
        print(f"  [Mercado Pago] Enviando {monto} {moneda} a {datos['cvu']}...")
        print(f"  [Mercado Pago] ✓ Transferencia enviada — ref: {referencia}")

        return {
            "exitoso": True,
            "referencia": referencia,
            "mensaje": f"Transferencia enviada a {datos['cvu']} (ref: {referencia})",
        }
