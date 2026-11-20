from flask import Flask, jsonify, request
import requests, os
from database import conectar

url_usuarios = os.getenv("USUARIOS_URL")
url_productos = os.getenv("PRODUCTOS_URL")

app = Flask(__name__)


@app.route("/pedidos")
def listar():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pedidos")
    pedidos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(pedidos)


@app.route("/pedidos/<int:id>/detalle")
def buscar(id):
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = "SELECT * FROM pedidos WHERE id = %s"
    cursor.execute(sql, (id,))
    pedido = cursor.fetchone()
    cursor.close()
    conexion.close()

    if pedido is None:
        return jsonify({"mensaje": "Pedido no encontrado"}), 404

    idUsuario = pedido["idUsuario"]
    idProducto = pedido["idProducto"]

    url_u= (
        os.getenv("USUARIOS_URL") + "/usuarios/"+ str(idUsuario))
    url_p= (
            os.getenv("PRODUCTOS_URL") + "/productos/"+ str(idProducto))

<<<<<<< Updated upstream
    try:
        usuario = requests.get(url_u)
    except requests.exceptions.ConnectionError:
        return jsonify({"mensaje": "Servicio de usuarios no esta disponible"}), 502
    try:
        producto = requests.get(url_p)
    except requests.exceptions.ConnectionError:
            return jsonify({"mensaje": "Servicio de productos no esta disponible"}), 502
=======
    def consultar(url, timeout, circuito, nombre):
        try:
            with circuito.calling():
                respuesta = requests.get(url, timeout=timeout)
                if respuesta.status_code >= 500:
                    respuesta.raise_for_status()
            return respuesta, None
        except pybreaker.CircuitBreakerError:
            return None, (f"Circuito abierto: {nombre} no disponible", 503)
        except requests.exceptions.Timeout:
            return None, (f"{nombre} tardó mucho tiempo en responder", 504)
        except requests.exceptions.ConnectionError:
            return None, (f"Servicio de {nombre} no está disponible", 503)
        except requests.exceptions.HTTPError:
            return None, (f"Error del servidor de {nombre}", 502)

    usuario, error_usuario = consultar(
        url_u, tiempo_maximo_u, circuito_usuarios, "Usuarios"
    )
    producto, error_producto = consultar(
        url_p, tiempo_maximo_p, circuito_productos, "Productos"
    )

    if error_usuario and error_producto:
        return jsonify({"mensaje": "Los servicios no están disponibles"}), 503
    if error_usuario:
        return jsonify({"mensaje": error_usuario[0]}), error_usuario[1]
    if error_producto:
        return jsonify({"mensaje": error_producto[0]}), error_producto[1]

    if usuario.status_code == 404:
        return jsonify({"mensaje": "Respuesta inesperada de usuarios"}), 404
    if usuario.status_code != 200:
        return jsonify({"mensaje": "Respuesta inesperada de usuarios"}), 502

    if producto.status_code == 404:
        return jsonify({"mensaje": "Respuesta inesperada de productos"}), 404
    if producto.status_code != 200:
        return jsonify({"mensaje": "Respuesta inesperada de productos"}), 502

>>>>>>> Stashed changes
    datosusuario = usuario.json()
    datospro = producto.json()
    return jsonify({
            "usuario": datosusuario.get("nombre"),
            "producto": datospro.get("nombre"),
            "cantidad": pedido["cantidad"],
            "estado": pedido["estado"],
            "valortotal": pedido["valortotal"],
            "fechaPedido": pedido["fechaPedido"]
        }), 200

<<<<<<< Updated upstream
=======
@app.route("/circuito/usuarios", methods=["GET"])
def estado_usuarios():
    return jsonify({
        "estado": circuito_usuarios.current_state.upper(),
        "fallos_consecutivos": circuito_usuarios.fail_counter,
        "umbral_fallos": circuito_usuarios.fail_max,
        "periodo_recuperacion": circuito_usuarios.reset_timeout
    })

@app.route("/circuito/productos", methods=["GET"])
def estado_productos():
    return jsonify({
        "estado": circuito_productos.current_state.upper(),
        "fallos_consecutivos": circuito_productos.fail_counter,
        "umbral_fallos": circuito_productos.fail_max,
        "periodo_recuperacion": circuito_productos.reset_timeout
    })

>>>>>>> Stashed changes

@app.route("/pedidos", methods=["POST"])
def crear():
    nuevoPedido = request.json
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)
    sql = """
        INSERT INTO pedidos
        (idUsuario, idProducto, cantidad, estado, valortotal, fechaPedido)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        nuevoPedido["idUsuario"],
        nuevoPedido["idProducto"],
        nuevoPedido["cantidad"],
        nuevoPedido["estado"],
        nuevoPedido["valortotal"],
        nuevoPedido["fechaPedido"]
    )
    cursor.execute(sql, valores)
    conexion.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Pedido creado", "id": nuevo_id}), 201


@app.route("/pedidos/<int:id>", methods=["DELETE"])
def eliminar(id):
    conexion = conectar()
    cursor = conexion.cursor()
    sql = "DELETE FROM pedidos WHERE id = %s"
    cursor.execute(sql, (id,))
    conexion.commit()
    filas_eliminadas = cursor.rowcount
    cursor.close()
    conexion.close()
    
    if filas_eliminadas == 0:
        return jsonify({"mensaje": "Pedido no encontrado"}), 404
        
    return jsonify({"mensaje": "Pedido eliminado correctamente"}), 200


@app.route("/pedidos/<int:id>", methods=["PUT"])
def actualizar_completo(id):
    datos = request.json
    
    campos_requeridos = ["idUsuario", "idProducto", "cantidad", "estado", "valortotal", "fechaPedido"]
    if not datos or not all(campo in datos for campo in campos_requeridos):
        return jsonify({"mensaje": "Faltan campos requeridos"}), 400

    conexion = conectar()
    cursor = conexion.cursor()
    
    sql = """
        UPDATE pedidos 
        SET idUsuario = %s, idProducto = %s, cantidad = %s, estado = %s, valortotal = %s, fechaPedido = %s
        WHERE id = %s
    """
    valores = (
        datos["idUsuario"],
        datos["idProducto"],
        datos["cantidad"],
        datos["estado"],
        datos["valortotal"],
        datos["fechaPedido"],
        id
    )
    
    cursor.execute(sql, valores)
    conexion.commit()
    
    filas_modificadas = cursor.rowcount
    cursor.close()
    conexion.close()
    
    if filas_modificadas == 0:
        return jsonify({"mensaje": "Pedido no encontrado o sin cambios"}), 404
        
    return jsonify({"mensaje": "Pedido actualizado correctamente"}), 200


@app.route("/pedidos/<int:id>", methods=["PATCH"])
def actualizar_parcial(id):
    datos = request.json
    
    if not datos:
        return jsonify({"mensaje": "No se enviaron datos para actualizar"}), 400

    campos = []
    valores = []

    if "idUsuario" in datos:
        campos.append("idUsuario = %s")
        valores.append(datos["idUsuario"])
        
    if "idProducto" in datos:
        campos.append("idProducto = %s")
        valores.append(datos["idProducto"])
        
    if "cantidad" in datos:
        campos.append("cantidad = %s")
        valores.append(datos["cantidad"])

    if "estado" in datos:
        campos.append("estado = %s")
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
        return jsonify({"mensaje": "Pedido no encontrado o sin cambios"}), 404
        
    return jsonify({"mensaje": "Pedido actualizado parcialmente"}), 200    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
