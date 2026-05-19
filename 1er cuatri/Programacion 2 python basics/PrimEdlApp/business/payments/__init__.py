"""
Auto-importa todas las implementaciones para que sus decoradores
@PaymentMethodRegistry.register() se ejecuten al iniciar el programa.
 
Para agregar un método nuevo: crear el archivo en esta carpeta
e importarlo acá. Una sola línea.
"""
 
from business.payments.base import PaymentMethod, PaymentMethodRegistry
 
# -- Implementaciones concretas --
from business.payments import mercadopago   # noqa: F401
from business.payments import tarjeta       # noqa: F401
# from business.payments import cripto      # ← ejemplo: descomentar al agregar
