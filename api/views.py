from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Usuario, Madre, Parto, RecienNacido, InformeREM
from .serializers import MadreSerializer, PartoSerializer, RecienNacidoSerializer, InformeREMSerializer
import bcrypt
import jwt
from datetime import datetime, timedelta, date
from django.db.models import Count

# Seguridad
from .auth import verificar_token, requiere_rol


CLAVE_SECRETA = "CLAVESECRETA12345"


# ============================
#       USUARIOS
# ============================

@api_view(['POST'])
def registrar_usuario(request):
    try:
        nombre = request.data.get('nombre')
        email = request.data.get('email')
        contraseña = request.data.get('contraseña')
        rol = request.data.get('rol')

        contraseña_hash = bcrypt.hashpw(contraseña.encode('utf-8'), bcrypt.gensalt())

        Usuario.objects.create(
            nombre=nombre,
            email=email,
            contraseña=contraseña_hash.decode('utf-8'),
            rol=rol
        )

        return Response({"mensaje": "Usuario registrado"}, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)



@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    contraseña = request.data.get('contraseña')

    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return Response({"error": "Usuario no existe"}, status=404)

    if bcrypt.checkpw(contraseña.encode('utf-8'), usuario.contraseña.encode('utf-8')):

        payload = {
            'id': usuario.id,
            'rol': usuario.rol,
            'exp': datetime.utcnow() + timedelta(hours=4)
        }

        token = jwt.encode(payload, CLAVE_SECRETA, algorithm='HS256')

        return Response({"token": token, "rol": usuario.rol}, status=200)

    return Response({"error": "Contraseña incorrecta"}, status=400)



# ============================
#         CRUD MADRE
# ============================

@api_view(['POST'])
@requiere_rol("admin", "matrona")
def crear_madre(request):
    serializer = MadreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@verificar_token
def listar_madres(request):
    madres = Madre.objects.all()
    serializer = MadreSerializer(madres, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@verificar_token
def obtener_madre(request, id):
    try:
        madre = Madre.objects.get(id=id)
        serializer = MadreSerializer(madre)
        return Response(serializer.data)
    except Madre.DoesNotExist:
        return Response({"error": "Madre no encontrada"}, status=404)


@api_view(['PUT'])
@requiere_rol("admin", "matrona")
def actualizar_madre(request, id):
    try:
        madre = Madre.objects.get(id=id)
    except Madre.DoesNotExist:
        return Response({"error": "Madre no encontrada"}, status=404)

    serializer = MadreSerializer(madre, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@requiere_rol("admin")
def eliminar_madre(request, id):
    try:
        madre = Madre.objects.get(id=id)
        madre.delete()
        return Response({"mensaje": "Madre eliminada correctamente"})
    except Madre.DoesNotExist:
        return Response({"error": "Madre no encontrada"}, status=404)



# ============================
#         CRUD PARTO
# ============================

@api_view(['POST'])
@requiere_rol("admin", "matrona")
def crear_parto(request):
    serializer = PartoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@verificar_token
def listar_partos(request):
    partos = Parto.objects.all()
    serializer = PartoSerializer(partos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@verificar_token
def obtener_parto(request, id):
    try:
        parto = Parto.objects.get(id=id)
        serializer = PartoSerializer(parto)
        return Response(serializer.data)
    except Parto.DoesNotExist:
        return Response({"error": "Parto no encontrado"}, status=404)


@api_view(['PUT'])
@requiere_rol("admin", "matrona")
def actualizar_parto(request, id):
    try:
        parto = Parto.objects.get(id=id)
    except Parto.DoesNotExist:
        return Response({"error": "Parto no encontrado"}, status=404)

    serializer = PartoSerializer(parto, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@requiere_rol("admin")
def eliminar_parto(request, id):
    try:
        parto = Parto.objects.get(id=id)
        parto.delete()
        return Response({"mensaje": "Parto eliminado correctamente"})
    except Parto.DoesNotExist:
        return Response({"error": "Parto no encontrado"}, status=404)



# ============================
#     CRUD RECIÉN NACIDO
# ============================

@api_view(['POST'])
@requiere_rol("admin", "matrona")
def crear_rn(request):
    serializer = RecienNacidoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['GET'])
@verificar_token
def listar_rn(request):
    rns = RecienNacido.objects.all()
    serializer = RecienNacidoSerializer(rns, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@verificar_token
def obtener_rn(request, id):
    try:
        rn = RecienNacido.objects.get(id=id)
        serializer = RecienNacidoSerializer(rn)
        return Response(serializer.data)
    except RecienNacido.DoesNotExist:
        return Response({"error": "RN no encontrado"}, status=404)


@api_view(['PUT'])
@requiere_rol("admin", "matrona")
def actualizar_rn(request, id):
    try:
        rn = RecienNacido.objects.get(id=id)
    except RecienNacido.DoesNotExist:
        return Response({"error": "RN no encontrado"}, status=404)

    serializer = RecienNacidoSerializer(rn, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
@requiere_rol("admin")
def eliminar_rn(request, id):
    try:
        rn = RecienNacido.objects.get(id=id)
        rn.delete()
        return Response({"mensaje": "RN eliminado correctamente"})
    except RecienNacido.DoesNotExist:
        return Response({"error": "RN no encontrado"}, status=404)



# ============================
#       REPORTE REM22
# ============================

@api_view(['GET'])
@requiere_rol("admin", "jefe_area", "medico")
def generar_informe_rem(request):

    fecha_actual = date.today()

    total_partos = Parto.objects.count()
    total_rn = RecienNacido.objects.count()

    partos_por_tipo = (
        Parto.objects.values("tipo_parto")
        .annotate(total=Count("tipo_parto"))
    )

    InformeREM.objects.create(
        fecha=fecha_actual,
        total_partos=total_partos,
        total_rn=total_rn
    )

    data = {
        "fecha": fecha_actual,
        "total_partos": total_partos,
        "total_rn": total_rn,
        "partos_por_tipo": list(partos_por_tipo),
        "mensaje": "Informe REM22 generado correctamente"
    }

    return Response(data, status=200)
