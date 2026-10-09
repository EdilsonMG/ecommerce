import mysql.connector
import os
import time

def conectar():
    for intento in range(10):
        try:
            conexion = mysql.connector.connect(
                host = os.getenv("USUARIOS_DB_HOST"),
                port = int(os.getenv("USUARIOS_DB_PORT", 3306)),
                user = os.getenv("USUARIOS_DB_USER"),
                password = os.getenv("USUARIOS_DB_PASSWORD"),
                database = os.getenv("USUARIOS_DB_NAME")
            )
            return conexion 
        except mysql.connector.error:
            print("La base de datos  aun esta cargando")
            intento + 1
            time.sleep(3)