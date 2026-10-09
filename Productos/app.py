from flask import Flask, jsonify, request
import requests, os
from database import conectar

app = Flask(__name__)



@app.route("/productos")
def listar():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM productos"
    )
    productos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(productos)


@app.route("/productos/<int:id>")
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql= """
        SELECT * FROM productos
        WHERE id =%s
    """
    cursor.execute(sql,(id,))
    producto = cursor.fetchone()
    cursor.close()
    conexion.close()
    if producto is None:
        return jsonify({"mensaje": "Producto no encontrado"}), 404
    return jsonify(producto)


@app.route("/productos", methods=["POST"])
def crear():
    nuevoProducto = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql=""""
        INSERT INTO productos
        (nombre, categoria, precio, stock)
        VALUES (%s, %s, %s, %s)
    """
    valores = (nuevoProducto["nombre"], nuevoProducto["categoria"], nuevoProducto["precio", nuevoProducto["stock"]])
    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje":"Producto creado", "id": nuevo_id}),201


@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()
    
    sql = """
        DELETE FROM mascotas
        WHERE id = %s
    """
    
    cursor.execute(sql, (id,))
    conexion.commit()
    
    filas_eliminadas = cursor.rowcount
    
    cursor.close()
    conexion.close()
    
    if filas_eliminadas == 0:
        return jsonify({"mensaje": "Producto no encontrado"}), 404
        
    return jsonify({"mensaje": "Producto eliminado correctamente"}), 200


@app.route("/productos/<int:id>", methods=["PUT"])
def actualizar_completo(id):
    datos = request.json
    
    if not datos or "nombre" not in datos or "categoria" not in datos or "precio" not in datos or "stock" not in datos:
        return jsonify({"mensaje": "Faltan campos requeridos"}), 400

    conexion = conectar()
    cursor = conexion.cursor()
    
    sql = """
        UPDATE productos
        SET nombre = %s, categoria = %s, precio = %s, stock = %s
        WHERE id = %s
    """
    valores = (datos["nombre"], datos["categoria"], datos["precio"], datos["stock"], id)
    
    cursor.execute(sql, valores)
    conexion.commit()
    
    filas_modificadas = cursor.rowcount
    cursor.close()
    conexion.close()
    
    if filas_modificadas == 0:
        return jsonify({"mensaje": "Producto no encontrado o sin cambios"}), 404
        
    return jsonify({"mensaje": "Producto actualizado correctamente"}), 200


@app.route("/productos/<int:id>", methods=["PATCH"])
def actualizar_parcial(id):
    datos = request.json
    
    if not datos:
        return jsonify({"mensaje": "No se enviaron datos para actualizar"}), 400

    campos = []
    valores = []

    if "nombre" in datos:
        campos.append("nombre = %s")
        valores.append(datos["nombre"])
        
    if "categoria" in datos:
        campos.append("categoria = %s")
        valores.append(datos["categoria"])
        
    if "precio" in datos:
        campos.append("precio = %s")
        valores.append(datos["precio"])

    if "stock" in datos:
            campos.append("stock = %s")
            valores.append(datos["stock"])    

    if not campos:
        return jsonify({"mensaje": "Campos no válidos"}), 400

    valores.append(id)
    
    sql = f"UPDATE mascotas SET {', '.join(campos)} WHERE id = %s"

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(sql, tuple(valores))
    conexion.commit()
    
    filas_modificadas = cursor.rowcount
    cursor.close()
    conexion.close()
    
    if filas_modificadas == 0:
        return jsonify({"mensaje": "Producto no encontrado o sin cambios"}), 404
        
    return jsonify({"mensaje": "Producto actualizado parcialmente"}), 200    

    
app.run (host="0.0.0.0", port= 5000)