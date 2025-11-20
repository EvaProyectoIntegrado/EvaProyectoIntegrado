# api/permissions.py
from django.http import JsonResponse
from functools import wraps
import jwt

CLAVE_SECRETA = "CLAVESECRETA12345"

def requiere_roles(*roles_permitidos):
    """
    Decorador que valida el rol del usuario usando el token JWT.
    Uso:
        @requiere_roles("matrona", "admin")
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            token = request.headers.get("Authorization")
            if not token:
                return JsonResponse({"success": False, "msg": "Token no enviado"}, status=401)

            try:
                token = token.replace("Bearer ", "")
                payload = jwt.decode(token, CLAVE_SECRETA, algorithms=["HS256"])
                rol_usuario = payload.get("rol")

                if rol_usuario not in roles_permitidos:
                    return JsonResponse({"success": False, "msg": "No autorizado"}, status=403)

                # Guardar datos del usuario para la vista
                request.usuario_id = payload.get("id")
                request.usuario_rol = rol_usuario

            except jwt.ExpiredSignatureError:
                return JsonResponse({"success": False, "msg": "Token expirado"}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({"success": False, "msg": "Token inválido"}, status=401)

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
