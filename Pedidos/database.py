import mysql.connector
import os
import time

def conectar():
    for intento in range(10):
        try:
            conexion = mysql.connector.connect(
                host = os.getenv("PEDIDOS_DB_HOST"),
                port = int(os.getenv("PEDIDOS_DB_PORT", 3306)),
                user = os.getenv("PEDIDOS_DB_USER"),
                password = os.getenv("PEDIDOS_DB_PASSWORD"),
                database = os.getenv("PEDIDOS_DB_NAME")
            )
            return conexion
        except mysql.connector.Error:
            print("La base de datos aun esta cargando")
            intento + 1
            time.sleep(3)
        
