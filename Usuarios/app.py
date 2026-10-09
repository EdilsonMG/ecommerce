from flask import Flask, jsonify, request
import requests, os
from database import conectar

app = Flask(__name__)


@app.route("/usuarios", methods=["GET"])
def listar():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM usuarios"
    )
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(usuarios)


@app.route("/usuarios/<int:id>", methods=["GET"])
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        SELECT * FROM usuarios
        WHERE id = %s
    """
    cursor.execute(sql, (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conexion.close()
    if usuario is None:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    return jsonify(usuario)


@app.route("/usuarios", methods=["POST"])
def crear():
    nuevoUsuario = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        INSERT INTO usuarios
        (nombre, email)
        VALUES (%s, %s)
    """
    valores = (nuevoUsuario["nombre"], nuevoUsuario["email"])
    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "usuario creado", "id": nuevo_id}), 201


@app.route("/usuarios/<int:id>", methods=["PUT"])
def actualizar_completo(id):
    datos = request.json
    
    if not datos or "nombre" not in datos or "email" not in datos:
        return jsonify({"mensaje": "Faltan campos requeridos"}), 400

    conexion = conectar()
    cursor = conexion.cursor()
    
    sql = """
        UPDATE usuarios 
        SET nombre = %s, email = %s
        WHERE id = %s
    """
    valores = (datos["nombre"], datos["email"], id)
    
    cursor.execute(sql, valores)
    conexion.commit()
    
    filas_modificadas = cursor.rowcount
    cursor.close()
    conexion.close()
    
    if filas_modificadas == 0:
        return jsonify({"mensaje": "Usuario no encontrado o sin cambios"}), 404
        
    return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200


@app.route("/usuarios/<int:id>", methods=["PATCH"])
def actualizar_parcial(id):
    datos = request.json
    
    if not datos:
        return jsonify({"mensaje": "No se enviaron datos para actualizar"}), 400

    campos = []
    valores = []

    if "nombre" in datos:
        campos.append("nombre = %s")
        valores.append(datos["nombre"])
        
    if "email" in datos:
        campos.append("email = %s")
        valores.append(datos["email"])

    if not campos:
        return jsonify({"mensaje": "Campos no válidos"}), 400

    valores.append(id)
    
    sql = f"UPDATE usuarios SET {', '.join(campos)} WHERE id = %s"

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(sql, tuple(valores))
    conexion.commit()
    
    filas_modificadas = cursor.rowcount
    cursor.close()
    conexion.close()
    
    if filas_modificadas == 0:
        return jsonify({"mensaje": "Usuario no encontrado o sin cambios"}), 404
        
    return jsonify({"mensaje": "Usuario actualizado parcialmente"}), 200


@app.route("/usuarios/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()
    
    sql = """
        DELETE FROM usuarios
        WHERE id = %s
    """
    
    cursor.execute(sql, (id,))
    conexion.commit()
    
    filas_eliminadas = cursor.rowcount
    
    cursor.close()
    conexion.close()
    
    if filas_eliminadas == 0:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
        
    return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200


app.run(host="0.0.0.0", port=5000)