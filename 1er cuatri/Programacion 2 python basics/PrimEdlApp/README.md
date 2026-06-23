# Financista MUY Juguete

Aplicación de billetera multi-moneda por línea de comandos, construida en Python con arquitectura en tres capas y dos implementaciones de persistencia intercambiables.

---

## Características

- **Cuentas multi-moneda**: abrí cuentas en cualquier divisa soportada por Fixer.io (USD, ARS, EUR, y más de 160 monedas).
- **Depósitos y extracciones** con validación de saldo.
- **Compra de moneda extranjera**: transferencias entre cuentas propias con conversión en tiempo real vía Fixer.io.
- **Historial de movimientos** filtrable por moneda.
- **Cotizaciones en vivo** con caché local para uso offline.
- **Métodos de pago extensibles**: Mercado Pago y Tarjeta de crédito/débito (con validación Luhn). Agregar un nuevo método no requiere tocar código existente.
- **Autenticación segura** con bcrypt y sanitización de usernames.
- **Persistencia intercambiable**: SQLObject (MySQL) o archivos JSON, configurable desde el `.env` sin modificar ninguna capa de la aplicación.

---

## Arquitectura

El proyecto sigue una arquitectura de tres capas estrictas:

```
presentation/   → Interfaz de usuario (menús CLI, inputs)
business/       → Lógica de negocio, validaciones, pagos
data/           → Acceso a datos (dos implementaciones intercambiables)
```

Cada capa depende únicamente de la inmediatamente inferior, y nunca de detalles de implementación concretos.

### Inversión de dependencias en la capa de datos

La capa de negocio (`business/`) depende exclusivamente de la abstracción `BaseDataHelper`, nunca de una implementación concreta:

```
business/Usuarios.py
    └── depende de → data/BaseDataHelper.py  (ABC)
                          ├── data/Usuarios.py       (implementación SQLObject)
                          └── data/FileDataHelper.py (implementación JSON)
```

El único lugar que conoce ambas implementaciones es `data/DataHelperFactory.py`, que se invoca desde `main.py`.

### Métodos de pago (`business/payments/`)

Usan el patrón **Registry + Factory**. Cada método hereda de `PaymentMethod` y se registra con un decorador:

```python
@PaymentMethodRegistry.register("mi_metodo")
class MiMetodoPago(PaymentMethod):
    display_name = "Mi Método"

    def solicitar_datos(self) -> dict: ...
    def procesar(self, monto, moneda, datos) -> dict: ...
```

El menú se construye dinámicamente; no hay que modificar nada más que el `__init__.py` del paquete.

---

## Estructura del proyecto

```
.
├── main.py
├── presentation/
│   └── Usuarios.py              # Menús y flujos de interacción
├── business/
│   ├── Usuarios.py              # Lógica de autenticación y movimientos
│   ├── Cotizacion.py            # Lógica de conversión de monedas
│   └── payments/
│       ├── base.py              # Clase base PaymentMethod + Registry
│       ├── mercadopago.py       # Implementación Mercado Pago (stub)
│       ├── tarjeta.py           # Implementación Tarjeta (con validación Luhn)
│       └── __init__.py          # Auto-registro de métodos de pago
└── data/
    ├── BaseDataHelper.py        # Interfaz abstracta (ABC) — contrato de la capa de datos
    ├── DataHelperFactory.py     # Factory: elige implementación según .env
    ├── Usuarios.py              # Implementación SQLObject (MySQL)
    ├── FileDataHelper.py        # Implementación con archivos JSON serializados
    ├── Models.py                # Modelos SQLObject (Usuario, Cuenta, Transaccion, Moneda)
    ├── Database.py              # Conexión y creación de tablas MySQL
    ├── Cotizacion.py            # Acceso a API Fixer.io y caché en BD
    └── __init__.py
```

---

## Requisitos

- Python 3.10+
- MySQL 5.7+ o MariaDB (solo si se usa `PERSISTENCE_BACKEND=sqlobject`)

### Dependencias Python

```
bcrypt
sqlobject
pymysql
requests
python-dotenv
tabulate
```

```bash
pip install bcrypt sqlobject pymysql requests python-dotenv tabulate
```

---

## Configuración

Creá un archivo `.env` en la raíz del proyecto:

```env
# Implementación de persistencia: "sqlobject" (MySQL) o "file" (JSON)
PERSISTENCE_BACKEND=sqlobject

# Conexión a MySQL (requerido solo si PERSISTENCE_BACKEND=sqlobject)
DB_HOST=localhost
DB_PORT=3306
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=financista

# API de cotizaciones (requerido siempre)
FIXERio_KEY=tu_api_key_de_fixer
```

Con `PERSISTENCE_BACKEND=sqlobject`, las tablas se crean automáticamente al iniciar si no existen.

Con `PERSISTENCE_BACKEND=file`, los datos se guardan en `data_files/` en la raíz del proyecto (se crea sola).

---

## Intercambio entre implementaciones de persistencia

Para cambiar de implementación basta con editar una línea del `.env`:

```env
PERSISTENCE_BACKEND=sqlobject   # usa MySQL vía SQLObject
PERSISTENCE_BACKEND=file        # usa archivos JSON en data_files/
```

No se modifica ningún archivo de código. El flujo es:

1. `main.py` llama a `DataHelperFactory.get_data_helper()`
2. El factory lee `PERSISTENCE_BACKEND` y devuelve una instancia de `BaseDataHelper`
3. Esa instancia se inyecta en `App` (presentación) → `LoginHelper` (negocio)
4. La lógica de negocio llama a `self.dh.getCuentas(...)`, `self.dh.saveCuentasYTransaccion(...)`, etc., sin saber qué hay debajo

Ambas implementaciones exponen exactamente la misma interfaz pública definida en `BaseDataHelper`.

---

## Ejecución

```bash
python main.py
```

Menú de acceso:

```
=======================================================
         Financista MUY Juguete
=======================================================
  1 - Iniciar sesión
  2 - Crear usuario
  0 - Salir
```

Una vez autenticado:

| Opción | Acción |
|--------|--------|
| 1 | Abrir cuenta en una moneda |
| 2 | Listar cuentas y saldos |
| 3 | Depositar fondos |
| 4 | Extraer fondos |
| 5 | Comprar moneda extranjera (transferencia con conversión) |
| 6 | Ver historial de movimientos |
| 7 | Ingresar fondos con Mercado Pago o Tarjeta |
| 8 | Retirar fondos vía Mercado Pago |
| 9 | Convertir monto entre monedas |
| 10 | Ver monedas disponibles |
| 11 | Actualizar lista de monedas (online) |

---

## Extender con un nuevo método de pago

1. Creá `business/payments/cripto.py`:

```python
from business.payments.base import PaymentMethod, PaymentMethodRegistry

@PaymentMethodRegistry.register("cripto")
class CriptoPayment(PaymentMethod):
    display_name = "Cripto (Bitcoin)"

    def solicitar_datos(self) -> dict:
        wallet = input("  Wallet > ").strip()
        return {"wallet": wallet}

    def procesar(self, monto, moneda, datos) -> dict:
        # Integrar con proveedor real acá
        return {"exitoso": True, "referencia": "TX-123", "mensaje": "Pago aprobado"}
```

2. Importalo en `business/payments/__init__.py`:

```python
from business.payments import cripto  # noqa: F401
```

El método aparece automáticamente en el menú.

---

## Notas técnicas

- Los métodos de pago son **stubs**: simulan aprobación instantánea. Para producción, reemplazar el cuerpo de `procesar()` con la llamada al SDK real del proveedor.
- La tarjeta valida el número con el algoritmo de **Luhn** y verifica la fecha de vencimiento.
- Las cotizaciones usan EUR como moneda base intermedia para cualquier par de divisas.
- Las contraseñas se almacenan **solo como hash bcrypt**, nunca en texto plano.
- La implementación con archivos usa **file-locking** (`fcntl`) para evitar condiciones de carrera en escrituras concurrentes.
