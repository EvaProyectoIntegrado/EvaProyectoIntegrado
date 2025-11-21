import jwt
from rest_framework.response import Response
from functools import wraps

CLAVE_SECRETA = "CLAVESECRETA12345"

def requiere_rol(*roles_permitidos):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):

            token = request.headers.get("Authorization")
            if not token:
                return Response({"error": "Token no proporcionado"}, status=401)

            try:
                token = token.replace("Bearer ", "")
                payload = jwt.decode(token, CLAVE_SECRETA, algorithms=["HS256"])

                rol = payload["rol"]

                if rol not in roles_permitidos:
                    return Response({"error": "No autorizado"}, status=403)

                request.usuario_id = payload["id"]
                request.usuario_rol = rol

            except jwt.ExpiredSignatureError:
                return Response({"error": "Token expirado"}, status=401)
            except jwt.InvalidTokenError:
                return Response({"error": "Token inválido"}, status=401)

            return func(request, *args, **kwargs)

        return wrapper
    return decorator

