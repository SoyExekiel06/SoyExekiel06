from sqlobject import (
    SQLObject,
    StringCol,
    DecimalCol,
    DateTimeCol,
    ForeignKey,
    MultipleJoin,
)
from datetime import datetime
 

 
class Usuario(SQLObject):
    """Almacena credenciales. Reemplaza users.json"""
 
    class sqlmeta:
        table = "usuario"
 
    username        = StringCol(length=100, notNone=True, unique=True)
    hashed_password = StringCol(length=255, notNone=True)
    created_at      = DateTimeCol(default=datetime.now)
 
    # Navegación inversa (no generan columnas en la tabla)
    cuentas       = MultipleJoin("Cuenta",      joinColumn="usuario_id")
    transacciones = MultipleJoin("Transaccion", joinColumn="usuario_id")
 
 
class Cuenta(SQLObject):
    """
    Un saldo por moneda por usuario.
    Reemplaza el campo 'cuentas' del JSON por usuario.
    """
 
    class sqlmeta:
        table = "cuenta"
 
    # ForeignKey → columna física: usuario_id  |  Python keyword: usuarioID
    usuario = ForeignKey("Usuario", dbName="usuarioid", notNone=True, cascade=True)
    moneda     = StringCol(length=10, notNone=True)
    # DECIMAL(20,8) para soportar cripto con muchos decimales
    saldo      = DecimalCol(size=20, precision=8, notNone=True, default=0)
    created_at = DateTimeCol(default=datetime.now)
 
 
class Transaccion(SQLObject):
    """
    Historial de movimientos.
    Reemplaza el campo 'historial' del JSON por usuario.
    """
 
    class sqlmeta:
        table = "transaccion"
 
    # ForeignKey → columna física: usuario_id  |  Python keyword: usuarioID
    usuario   = ForeignKey("Usuario", notNone=True, cascade=True)
    tipo      = StringCol(length=30, notNone=True)   # apertura|deposito|extraccion|transferencia
    timestamp = DateTimeCol(notNone=True)
 
    # Campos comunes (NULL cuando no aplican al tipo de movimiento)
    moneda            = StringCol(length=10,    default=None)
    monto             = DecimalCol(size=20, precision=8, default=None)
    saldo_resultante  = DecimalCol(size=20, precision=8, default=None)
 
    # Campos exclusivos de transferencia entre monedas
    moneda_origen             = StringCol(length=10,    default=None)
    monto_origen              = DecimalCol(size=20, precision=8, default=None)
    saldo_origen_resultante   = DecimalCol(size=20, precision=8, default=None)
    moneda_destino            = StringCol(length=10,    default=None)
    monto_destino             = DecimalCol(size=20, precision=8, default=None)
    saldo_destino_resultante  = DecimalCol(size=20, precision=8, default=None)
 
    # Campos de pago externo (depósito via tarjeta / MercadoPago)
    metodo_pago      = StringCol(length=50,  default=None)
    referencia_pago  = StringCol(length=100, default=None)
 
 
class Moneda(SQLObject):
    """
    Caché de monedas obtenidas desde Fixer.
    Reemplaza monedas.json.
    """
 
    class sqlmeta:
        table = "moneda"
 
    codigo     = StringCol(length=10,  notNone=True, unique=True)
    nombre     = StringCol(length=150, notNone=True)
    updated_at = DateTimeCol(default=datetime.now)