from flask import Blueprint, request, jsonify
from .zk_connector import get_assists, deleted_assists
from .auth import require_token

main = Blueprint('main', __name__)


@main.route("/", methods=["GET"])
def hello():
    return "App Corriendo en local"


@main.route("/asistencias", methods=["POST"])
@require_token
def asistencias():
    try:
        body = request.get_json()

        ip = body.get("ip")
        port = int(body.get("port",4370))
        password = int(body.get("password",0))

        if not ip:
            return jsonify({"status": "error", "message": "Falta el parámetro 'ip'"}), 400
        
        data = get_assists(ip,port,password)
        count = len(data)
        return jsonify({"status": "ok", "asistencias": data, "quantity": count}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    

@main.route("/asistencias/borrar", methods=["POST"])
@require_token
def borrar_asistencias():
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Content-Type debe ser application/json"
        }), 415
    
    try:
        body = request.get_json()
        ip = body.get("ip")
        port = int(body.get("port", 4370))
        password = int(body.get("password", 0))
        cantidad = int(body.get("quantity", -1))

        if not ip or cantidad < 0:
            return jsonify({"status": "error", "message": "Parámetros inválidos"}), 400

        resultado = deleted_assists(ip, port, password, cantidad)
        status_code = 200 if resultado["status"] == "ok" else 409
        return jsonify(resultado), status_code

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500