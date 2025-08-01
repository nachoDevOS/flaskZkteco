from functools import wraps
from flask import request, jsonify
import os

API_TOKEN = os.getenv("TOKEN")

def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        client_token = request.headers.get("X-API-TOKEN")
        if not client_token or client_token != API_TOKEN:
            return jsonify({"status": "error", "message": "Token inválion o ausente"}), 401
        return func(*args,**kwargs)
    return wrapper