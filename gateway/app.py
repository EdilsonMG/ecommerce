from flask import Flask, jsonify, Response, request
import os
import requests

app = Flask(__name__)

USUARIOS_URL = os.getenv("USUARIOS_URL", "http://usuarios:5000" )
PRODUCTOS_URL = os.getenv("PRODUCTOS_URL", "http://productos:50000" )
PEDIDOS_URL = os.getenv("PEDIDOS_URL", "http://pedidos:5000")

def reenviar(metodo, url):
    try:
        respuesta = requests.request(metodo, url, params=request.args, json=request.get_json(silent=True), timeout=5)
        return Response(respuesta.content, status=respuesta.status_code, content_type= respuesta.headers.get("Content-Type", "application/json"))
    except request.exceptions.Timeout:
        return jsonify({
            "mensaje": "El servicio destino tardo en responder"
        }), 504
    except request.exceptions.ConnectionError:
        return jsonify({
            "mensaje": "No fue posibe conectar con el servicio vecino"
        }), 503


@app.route("/productos",methods = ["GET", "POST", "PATCH"])
def ruta_producto():
    return reenviar(request.method, PRODUCTOS_URL + "/productos")
app.run(host="0.0.0.0", port = 5000)

@app.route("/productos/<path:ruta>", methods=["GET", "DELETE"])
def ruta_producto_detalle(ruta):
    return reenviar(request.method, PRODUCTOS_URL + "/productos/" + ruta)