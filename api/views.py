from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

from .models import Usuario, Madre, Parto, RecienNacido

# =========================================================
#                 REGISTRO DE USUARIO
# =========================================================
@csrf_exempt
def registrar_usuario(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "msg": "Método no permitido"})

    data = json.loads(request.body)

    nombre = data.get("nombre")
    email = data.get("email")
    contraseña = data.get("contraseña")
    rol = data.get("rol")

    if not nombre or not email or not contraseña or not rol:
        return JsonResponse({"success": False, "msg": "Campos incompletos"})

    if Usuario.objects.filter(email=email).exists():
        return JsonResponse({"success": False, "msg": "El email ya está registrado"})

    usuario = Usuario.objects.create(
        nombre=nombre,
        email=email,
        contraseña=make_password(contraseña),
        rol=rol
    )

    return JsonResponse({"success": True, "msg": "Usuario registrado", "id": usuario.id})


# =========================================================
#                 LOGIN
# =========================================================
@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "msg": "Método no permitido"})

    data = json.loads(request.body)
    email = data.get("usuario")
    password = data.get("password")

    try:
        usuario = Usuario.objects.get(email=email)
        if check_password(password, usuario.contraseña):
            return JsonResponse({"success": True, "usuario": usuario.nombre})
        else:
            return JsonResponse({"success": False, "msg": "Contraseña incorrecta"})
    except Usuario.DoesNotExist:
        return JsonResponse({"success": False, "msg": "Usuario no existe"})


# =========================================================
#                       MADRES CRUD
# =========================================================

def listar_madres(request):
    madres = list(Madre.objects.values())
    return JsonResponse(madres, safe=False)


@csrf_exempt
def crear_madre(request):
    data = json.loads(request.body)

    madre = Madre.objects.create(
        rut=data["rut"],
        nombre=data["nombre"],
        edad=data["edad"],
        direccion=data["direccion"]
    )
    return JsonResponse({"msg": "Madre creada", "id": madre.id})


def obtener_madre(request, id):
    try:
        m = Madre.objects.get(id=id)
        return JsonResponse({
            "id": m.id,
            "rut": m.rut,
            "nombre": m.nombre,
            "edad": m.edad,
            "direccion": m.direccion
        })
    except Madre.DoesNotExist:
        return JsonResponse({"msg": "Madre no encontrada"})


@csrf_exempt
def actualizar_madre(request, id):
    try:
        m = Madre.objects.get(id=id)
    except Madre.DoesNotExist:
        return JsonResponse({"msg": "Madre no existe"})

    data = json.loads(request.body)
    m.rut = data.get("rut", m.rut)
    m.nombre = data.get("nombre", m.nombre)
    m.edad = data.get("edad", m.edad)
    m.direccion = data.get("direccion", m.direccion)
    m.save()

    return JsonResponse({"msg": "Madre actualizada"})


@csrf_exempt
def eliminar_madre(request, id):
    try:
        m = Madre.objects.get(id=id)
        m.delete()
        return JsonResponse({"msg": "Madre eliminada"})
    except Madre.DoesNotExist:
        return JsonResponse({"msg": "Madre no existe"})


# =========================================================
#                     PARTOS CRUD
# =========================================================

def listar_partos(request):
    partos = []
    for p in Parto.objects.all():
        partos.append({
            "id": p.id,
            "madre": p.madre.id,
            "madre_nombre": p.madre.nombre,
            "fecha_parto": str(p.fecha_parto),
            "tipo_parto": p.tipo_parto,
            "observaciones": p.observaciones
        })
    return JsonResponse(partos, safe=False)


@csrf_exempt
def crear_parto(request):
    data = json.loads(request.body)
    madre = Madre.objects.get(id=data["madre"])

    parto = Parto.objects.create(
        madre=madre,
        fecha_parto=data["fecha_parto"],
        tipo_parto=data["tipo_parto"],
        observaciones=data.get("observaciones", "")
    )

    return JsonResponse({"msg": "Parto registrado", "id": parto.id})


def obtener_parto(request, id):
    try:
        p = Parto.objects.get(id=id)
        return JsonResponse({
            "id": p.id,
            "madre": p.madre.id,
            "madre_nombre": p.madre.nombre,
            "fecha_parto": str(p.fecha_parto),
            "tipo_parto": p.tipo_parto,
            "observaciones": p.observaciones,
        })
    except Parto.DoesNotExist:
        return JsonResponse({"msg": "Parto no existe"})


@csrf_exempt
def actualizar_parto(request, id):
    try:
        p = Parto.objects.get(id=id)
    except Parto.DoesNotExist:
        return JsonResponse({"msg": "Parto no existe"})

    data = json.loads(request.body)

    if "madre" in data:
        p.madre = Madre.objects.get(id=data["madre"])

    p.fecha_parto = data.get("fecha_parto", p.fecha_parto)
    p.tipo_parto = data.get("tipo_parto", p.tipo_parto)
    p.observaciones = data.get("observaciones", p.observaciones)
    p.save()

    return JsonResponse({"msg": "Parto actualizado"})


@csrf_exempt
def eliminar_parto(request, id):
    try:
        p = Parto.objects.get(id=id)
        p.delete()
        return JsonResponse({"msg": "Parto eliminado"})
    except Parto.DoesNotExist:
        return JsonResponse({"msg": "Parto no existe"})


# =========================================================
#                  RN CRUD
# =========================================================

def listar_rn(request):
    data = list(RecienNacido.objects.values())
    return JsonResponse(data, safe=False)


@csrf_exempt
def crear_rn(request):
    data = json.loads(request.body)
    parto = Parto.objects.get(id=data["parto"])

    rn = RecienNacido.objects.create(
        parto=parto,
        peso=data["peso"],
        talla=data["talla"],
        apgar=data["apgar"]
    )

    return JsonResponse({"msg": "RN creado", "id": rn.id})


def obtener_rn(request, id):
    try:
        r = RecienNacido.objects.get(id=id)
        return JsonResponse({
            "id": r.id,
            "parto": r.parto.id,
            "peso": r.peso,
            "talla": r.talla,
            "apgar": r.apgar
        })
    except RecienNacido.DoesNotExist:
        return JsonResponse({"msg": "RN no existe"})


@csrf_exempt
def actualizar_rn(request, id):
    try:
        r = RecienNacido.objects.get(id=id)
    except RecienNacido.DoesNotExist:
        return JsonResponse({"msg": "RN no existe"})

    data = json.loads(request.body)

    r.peso = data.get("peso", r.peso)
    r.talla = data.get("talla", r.talla)
    r.apgar = data.get("apgar", r.apgar)
    r.save()

    return JsonResponse({"msg": "RN actualizado"})


@csrf_exempt
def eliminar_rn(request, id):
    try:
        r = RecienNacido.objects.get(id=id)
        r.delete()
        return JsonResponse({"msg": "RN eliminado"})
    except RecienNacido.DoesNotExist:
        return JsonResponse({"msg": "RN no existe"})


# =========================================================
#                    PDF REM22
# =========================================================
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def descargar_rem22(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Informe_REM22.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(40, height - 40, "Informe Clínico – REM22")

    total_madres = Madre.objects.count()
    total_partos = Parto.objects.count()
    total_rn = RecienNacido.objects.count()

    pdf.setFont("Helvetica", 12)
    pdf.drawString(40, height - 80, f"Madres registradas: {total_madres}")
    pdf.drawString(40, height - 100, f"Partos registrados: {total_partos}")
    pdf.drawString(40, height - 120, f"Recién nacidos: {total_rn}")

    pdf.showPage()
    pdf.save()

    return response
