from django.http import JsonResponse
import jwt

CLAVE_SECRETA = "CLAVESECRETA12345"

def requiere_rol(*roles_permitidos):
    def decorator(func):
        def wrapper(request, *args, **kwargs):

            token = request.headers.get("Authorization", "").replace("Bearer ", "")

            if not token:
                return JsonResponse({"error": "Token no proporcionado"}, status=401)

            try:
                data = jwt.decode(token, CLAVE_SECRETA, algorithms=["HS256"])
            except:
                return JsonResponse({"error": "Token inválido"}, status=401)

            # VALIDAR ROL
            if data["rol"] not in roles_permitidos:
                return JsonResponse({"error": "No autorizado"}, status=403)

            # Guardar usuario en la request
            request.usuario = data

            return func(request, *args, **kwargs)
        return wrapper
    return decorator

