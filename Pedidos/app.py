from flask import Flask, jsonify, request
import requests, os
from database import conectar

url_usuarios = os.getenv("USUARIOS_URL")

app = Flask(__name__)



@app.route("/pedidos")
def listar():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM pedidos"
    )
    mascotas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(mascotas)


@app.route("/pedidos/<int:id>")
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql= """
        SELECT * FROM pedidos
        WHERE id =%s
    """
    cursor.execute(sql,(id,))
    pedido = cursor.fetchone()
    cursor.close()
    conexion.close()
    if pedido is None:
        return jsonify({"mensaje": "Pedido no encontrado"}), 404
    return jsonify(pedido)


@app.route("/pedidos", methods=["POST"])
def crear():
    nuevoPedido= request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql=""""
        INSERT INTO pedidos
        (idUsuario,idProducto, cantidad, estado, valortotal, fechaPedido)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (nuevoPedido["idUsuario"], nuevoPedido["idProdcuto"], nuevoPedido["cantidad"], nuevoPedido["estado"], nuevoPedido["valortotal"], nuevoPedido["fechaPedido"])
    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje":"pedido creado", "id": nuevo_id}),201


@app.route("/pedidos/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()
    
    sql = """
        DELETE FROM pedidos
        WHERE id = %s
    """
    
    cursor.execute(sql, (id,))
    conexion.commit()
    
    filas_eliminadas = cursor.rowcount
    
    cursor.close()
    conexion.close()
    
    if filas_eliminadas == 0:
        return jsonify({"mensaje": "Pedido no encontrado"}), 404
        
    return jsonify({"mensaje": "Pedido eliminado correctamente"}), 200


@app.route("/mascotas/<int:id>", methods=["PUT"])
def actualizar_completo(id):
    datos = request.json
    
    if not datos or "idUsuario" not in datos or "idProducto" not in datos or "cantidad" not in datos or "estado" not in datos or "valortotal" not in datos or "fechaPedido" not in datos:
        return jsonify({"mensaje": "Faltan campos requeridos"}), 400

    conexion = conectar()
    cursor = conexion.cursor()
    
    sql = """
        UPDATE mascotas 
        SET idUsuario = %s, idProducto= %s, cantidad = %s, estado = %s, valortotal = %s, fechaPedido= %s
        WHERE id = %s
    """
    valores = ((datos["idUsuario"], datos["idProdcuto"], datos["cantidad"], datos["estado"], datos["valortotal"], datos["fechaPedido"]), id)
    
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

    if "idUsuario" in datos:
        campos.append("idUsuario = %s")
        valores.append(datos["idUsuario"])
        
    if "idProdcuto" in datos:
        campos.append("idProducto = %s")
        valores.append(datos["idProducto"])
        
    if "cantidad" in datos:
        campos.append("cantidad = %s")
        valores.append(datos["cantidad"])

    if "estado" in datos:
            campos.append("estado= %s")
            valores.append(datos["estado"])

    if "valortotal" in datos:
            campos.append("valortotal = %s")
            valores.append(datos["valortotal"])

    if "fechaPedido" in datos:
            campos.append("fechaPedido = %s")
            valores.append(datos["fechaPedido"])

    if not campos:
        return jsonify({"mensaje": "Campos no válidos"}), 400

    valores.append(id)
    
    sql = f"UPDATE pedidos SET {', '.join(campos)} WHERE id = %s"

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(sql, tuple(valores))
    conexion.commit()
    
    filas_modificadas = cursor.rowcount
    cursor.close()
    conexion.close()
    
    if filas_modificadas == 0:
        return jsonify({"mensaje": "Pedido no encontrado sin cambios"}), 404
        
    return jsonify({"mensaje": "Pedido actualizado parcialmente"}), 200    

    
app.run (host="0.0.0.0", port= 5000)