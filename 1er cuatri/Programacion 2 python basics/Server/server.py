from flask import Flask, jsonify, request
from data import getCurrencies, getCurrency
import json

app = Flask(__name__)
@app.route("/monedas", methods = ["GET"])
def obtenerMonedas():
    monedas = getCurrencies()
    respuesta = {"monedas" : monedas}
    return jsonify(respuesta)

@app.route("/cotizacion", methods = ["GET"])
def obtenerCotizacion():
    codigo = request.args.get("codigo")
    if codigo is None:
        return jsonify({"Error" : "tenes que pasar el codigo"}), 400
    cotizacion = getCurrency(codigo)
    if cotizacion is None:
        return jsonify({"Error" : "No existe es moneda"}), 404
    respuesta = { codigo : cotizacion}
    return jsonify(respuesta)

@app.route("/cotizacion", methods = ["POST"])
def obtenerCotizacion_Post():

    body = json.loads(request.get_json())

    try:
        codigo = body["codigo"]
    except KeyError:
        return jsonify({"Error" : "Tienes que pasarme el codigo"}),400
    if codigo is None:
        return jsonify({"Error" : "Tienes que pasarme el codigo"}),400
    cotizacion = getCurrency(codigo)
    if cotizacion is None:
        return jsonify({"Error" : "no existe esta moneda"}), 404
    response = {codigo:cotizacion}
    return jsonify(response)
    

    # if codigo is None:
    #     return jsonify({"Error" : "tenes que pasar el codigo"}), 400
    # cotizacion = getCurrency(codigo)
    # if cotizacion is None:
    #     return jsonify({"Error" : "No existe es moneda"}), 404
    # respuesta = { codigo : cotizacion}
    # return jsonify(respuesta)


if __name__ == "__main__":
    app.run(port = 20220, debug = True)