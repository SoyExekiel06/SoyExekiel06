import os
import dotenv
from sqlobject import connectionForURI, sqlhub
from data import Models as m
dotenv.load_dotenv()
 
 
def get_connection_uri() -> str:
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    return f"mysql://{user}:{password}@{host}:{port}/{database}"
 
 
def init_db():
    """
    Establece la conexión global de SQLObject y crea las tablas si no existen.
    Llamar una sola vez al arrancar la aplicación.
    """
    uri = get_connection_uri()
    __connection__ = connectionForURI(uri)
    sqlhub.processConnection = __connection__

    for tabla in (m.Usuario, m.Cuenta, m.Transaccion, m.Moneda):
        tabla.createTable(ifNotExists=True)

    print(m.Cuenta)
    print(m.Cuenta.__module__)
    print(m.Cuenta.sqlmeta.columns.keys())