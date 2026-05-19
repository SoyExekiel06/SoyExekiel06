"""Sistema de métodos de pago extensible.
 
Para agregar un nuevo método:
1. Crear un archivo en business/payments/
2. Heredar de PaymentMethod
3. Decorar la clase con @PaymentMethodRegistry.register("nombre")
 
No hay que tocar ningún otro archivo.
"""
 
from abc import ABC, abstractmethod
from decimal import Decimal
 
 
class PaymentMethod(ABC):
    """
    Contrato que todo método de pago debe cumplir.
    """
 
    # Nombre legible para mostrar en menú (sobreescribir en subclase)
    display_name: str = "Método desconocido"
 
    @abstractmethod
    def solicitar_datos(self) -> dict:
        """
        Interactúa con el usuario para recolectar los datos necesarios
        (número de tarjeta, referencia de pago, etc.).
        Devuelve un dict con los datos recolectados.
        """
        ...
 
    @abstractmethod
    def procesar(self, monto: Decimal, moneda: str, datos: dict) -> dict:
        """
        Ejecuta el cobro/verificación con el proveedor externo (o simula).
        Devuelve un dict con al menos:
            - "exitoso": bool
            - "referencia": str  (ID de transacción, comprobante, etc.)
            - "mensaje": str     (texto para mostrar al usuario)
        Lanza ValueError si hay un problema de validación previo al cobro.
        """
        ...
    def acreditar(self, monto: Decimal, moneda: str, datos: dict) -> dict:
        raise NotImplementedError(
            f"'{self.display_name}' no soporta egresos de fondos."
        )
 
class PaymentMethodRegistry:
    """
    Factory + Registry de métodos de pago.
    Auto-descubre subclases registradas con @PaymentMethodRegistry.register().
    """
 
    _registry: dict[str, type[PaymentMethod]] = {}
 
    @classmethod
    def register(cls, key: str):
        """
        Decorador para registrar un método de pago.
 
        Uso:
            @PaymentMethodRegistry.register("mercadopago")
            class MercadoPagoPayment(PaymentMethod):
                ...
        """
        def decorator(payment_cls: type[PaymentMethod]):
            cls._registry[key.lower()] = payment_cls
            return payment_cls
        return decorator
 
    @classmethod
    def create(cls, key: str) -> PaymentMethod:
        """Instancia el método de pago por su clave. Lanza KeyError si no existe."""
        key = key.lower()
        if key not in cls._registry:
            raise KeyError(
                f"Método de pago '{key}' no registrado. "
                f"Disponibles: {list(cls._registry.keys())}"
            )
        return cls._registry[key]()
 
    @classmethod
    def disponibles(cls) -> list[tuple[str, str]]:
        """Devuelve [(clave, display_name), ...] para construir menús dinámicamente."""
        return [
            (key, klass.display_name)
            for key, klass in cls._registry.items()
        ]
