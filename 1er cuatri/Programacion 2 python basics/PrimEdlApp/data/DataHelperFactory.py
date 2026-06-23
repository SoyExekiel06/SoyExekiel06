"""
Factory de la capa de datos.
 
Lee la variable de entorno PERSISTENCE_BACKEND y devuelve
la implementación correspondiente de BaseDataHelper.
 
Valores válidos de PERSISTENCE_BACKEND:
    "sqlobject"  →  dataHelper       (base de datos MySQL via SQLObject)
    "file"       →  FileDataHelper   (archivos JSON serializados)
 
Si la variable no está definida, se usa SQLObject por defecto.
 
Uso desde la capa de negocio o desde main:
    from data.DataHelperFactory import get_data_helper
    dh = get_data_helper()
"""
 
import os
import dotenv
 
dotenv.load_dotenv()
 
from .BaseDataHelper import BaseDataHelper
 
 
def get_data_helper() -> BaseDataHelper:
    backend = os.getenv("PERSISTENCE_BACKEND", "sqlobject").strip().lower()
 
    if backend == "file":
        from .FileDataHelper import FileDataHelper
        return FileDataHelper()
 
    elif backend == "sqlobject":
        from . import Database
        Database.init_db()
        from .Usuarios import dataHelper
        return dataHelper()
 
    else:
        raise EnvironmentError(
            f"PERSISTENCE_BACKEND='{backend}' no es válido. "
            "Usá 'sqlobject' o 'file'."
        )