# Flask ZKteco

Microservicio para manejar dispositivos Biometricos ZKteco. Version previa

## Requisitos

- Python > 3.11

## Instalación

Clonar el proyecto:

```bash
  git clone https://github.com/Andonny1up/flaskZkteco.git
```

Crear un entornor virtual desde la carpeta raiz del proyecto:

```bash
  python -m venv venv
```

Activar el entorno virtual

```bash
  ./venv/Scripts/activate
```

Instalar las dependencias

```bash
  pip install -r requirements.txt
```

Copiar el archivo .env.example a .env

| Variables | Description                                                                               |
| :-------- | :---------------------------------------------------------------------------------------- |
| `PORT`    | Puerto en el que se desplegara la app                                                     |
| `TOKEN`   | **Requerido**. Token secreto. Se utiliza para aceptar peticiones que solo tengan el token |

```bash
  pip install -r requirements.txt
```

Correr el programa:

```bash
  python run.py
```

## Referencia de la API

Enviar en el HEADER el TOKEN:

```http
  -H "X-API-TOKEN: XXXXXXXXXX"
```

### obtener asistencias

Conten type: json

```http
  POST /asistencias
```

#### Ejemplo de Cuerpo:

```http
{
  "ip": "192.xxx.xxx.xx",
  "port": 4370,
  "password": xxxxx
}
```

### Ejemplo con curl:

```bash
curl -X POST http://localhost:5000/asistencias \
  -H "Content-Type: application/json" \
  -H "X-API-TOKEN: XXXXXXXXXX" \
  -d '{"ip": "192.xxx.xxx.xxx", "port": 4370, "password": xxxx}
```

### Borrar asistencias

Conten type: json

```http
  POST /asistencias/borrar
```

#### Ejemplo de Cuerpo:

Se necesita enviar la cantidad exacta de los registros por seguridad, se puede obtener de /asistencias

```http
{
  "ip": "192.xxx.xxx.xx",
  "port": 4370,
  "password": xxxxx,
  "quantity": x
}
```
