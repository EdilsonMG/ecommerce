from flask import Flask, jsonify, Response, request
import os
import requests

app = Flask(__name__)

USUARIOS_URL = os.getenv("USUARIOS_URL", "http://usuarios:5000" )
PRODUCTOS_URL = os.getenv("PRODUCTOS_URL", "http://productos:50000" )
PEDIDOS_URL = os.getenv("PEDIDOS_URL", "http://pedidos:5000")

def reeenviar(metodo, url):
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

@app.route("/usuarios",methods = ["GET", "POST"])
def ruta_usuario():
    return reeenviar(request.method, USUARIOS_URL + "/usuarios")
app.run(host="0.0.0.0", port = 5000)