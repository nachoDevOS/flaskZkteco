from zk import ZK
from datetime import datetime
import json
import os


def get_assists(ip, port, password):
    zk = ZK(ip, port=port, timeout=5, password=password)

    conn = zk.connect()
    conn.disable_device()
    attendance = conn.get_attendance()
    conn.enable_device()
    conn.disconnect()

    data = []

    for record in attendance:
        data.append({
            "user_id": record.user_id,
            "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "status": record.status
        })

    return data

def deleted_assists(ip, port, password, quatity):
    zk = ZK(ip, port=port, timeout=5, password=password)

    conn = zk.connect()
    conn.disable_device()
    attendance = conn.get_attendance()

    if len(attendance) == 0:
        conn.enable_device()
        conn.disconnect()
        return {
            "status": "ok",
            "message": "No hay asistencias que borrar.",
            "backup": None
        }
    
    if len(attendance) != quatity:
        conn.enable_device()
        conn.disconnect()
        return {
            "status": "error",
            "message": f"La cantidad actual ({len(attendance)}) no coincide con la esperada ({quatity}). Borrado cancelado.",
            "backup": None
        }
    # crear backup
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"backup_asistencias_{ip.replace('.', '-')}_{now}.json"
    os.makedirs("backups", exist_ok=True)
    backup_path = os.path.join("backups", filename)

    data = [{
        "user_id": r.user_id,
        "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "status": r.status
    } for r in attendance]

    with open(backup_path, "w") as f:
        json.dump(data, f, indent=2)

    # Borrar asistencia
    conn.clear_attendance()
    conn.enable_device()
    conn.disconnect()
    
    return {
        "status": "ok",
        "message": f"Se borraron {len(attendance)} asistencias tras verificación exitosa.",
        "backup": backup_path
    }