# REEMPLAZA TODO TU ARCHIVO views.py CON ESTE CÓDIGO CORREGIDO

from django.shortcuts import render, redirect, get_object_or_404
from api.models import Usuario, Madre, Parto, RecienNacido
from datetime import datetime
from django.utils import timezone
from django.db.models import Count, Avg
from datetime import timedelta
import json

# ==================== LISTAS ====================

def madres_list(request):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "medico", "jefe_area", "admin"]:
        return redirect("/login/")

    madres = Madre.objects.all()
    rol = request.session.get("rol")
    
    if rol == "medico":
        return render(request, "madres_medico.html", {"madres": madres})
    else:
        return render(request, "madres.html", {"madres": madres})


def partos_list(request):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "medico", "jefe_area", "admin"]:
        return redirect("/login/")

    partos = Parto.objects.all()
    rol = request.session.get("rol")
    
    if rol == "medico":
        return render(request, "partos_medico.html", {"partos": partos})
    else:
        return render(request, "partos.html", {"partos": partos})


def rn_view(request):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "medico", "admin"]:
        return redirect("/login/")

    partos = Parto.objects.all()
    rn_list = RecienNacido.objects.all()
    error = None

    if request.method == "POST":
        parto_id = request.POST.get("parto")
        peso = float(request.POST.get("peso"))
        talla = float(request.POST.get("talla"))
        apgar = int(request.POST.get("apgar"))
        sexo = request.POST.get("sexo")

        # Validaciones
        if peso < 0.5 or peso > 6:
            error = "❌ El peso debe estar entre 0.5 y 6 kg."
        elif talla < 40 or talla > 60:
            error = "❌ La talla debe estar entre 40 y 60 cm."
        elif apgar < 0 or apgar > 10:
            error = "❌ El APGAR debe estar entre 0 y 10."
        else:
            parto = get_object_or_404(Parto, id=parto_id)

            if hasattr(parto, "rn"):
                error = "❌ Este parto ya tiene un RN registrado."

            if not error:
                RecienNacido.objects.create(
                    parto=parto,
                    peso=peso,
                    talla=talla,
                    apgar=apgar,
                    sexo=sexo
                )
                return redirect("/rn/")

    context = {
        "partos": partos,
        "rn_list": rn_list,
        "error": error,
    }
    
    # Cargar template según el rol
    rol = request.session.get("rol")
    
    if rol == "medico":
        return render(request, "rn_medico.html", context)
    else:
        return render(request, "rn.html", context)


def usuarios_view(request):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["jefe_area", "admin"]:
        return redirect("/dashboard/")
        
    usuarios = Usuario.objects.all()
    return render(request, "usuarios.html", {"usuarios": usuarios})


# ==================== LOGIN Y REGISTRO ====================

def login_view(request):
    return render(request, "login.html")


def register_view(request):
    return render(request, "registrar.html")


# ==================== DASHBOARD ====================

def dashboard(request):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    # Obtener estadísticas
    total_madres = Madre.objects.count()
    total_partos = Parto.objects.count()
    total_rn = RecienNacido.objects.count()
    
    mes_actual = datetime.now().month
    partos_mes = Parto.objects.filter(fecha_parto__month=mes_actual).count()
    
    context = {
        'total_madres': total_madres,
        'total_partos': total_partos,
        'total_rn': total_rn,
        'partos_mes': partos_mes,
    }
    
    # Cargar template según el rol
    rol = request.session.get("rol")
    
    if rol == "matrona":
        return render(request, "dashboard_matrona.html", context)
    elif rol == "medico":
        return render(request, "dashboard_medico.html", context)
    elif rol == "jefe_area":
        return render(request, "dashboard_jefe.html", context)
    elif rol == "admin":
        return render(request, "dashboard_admin.html", context)
    else:
        return render(request, "dashboard.html", context)


# ==================== MADRES CRUD ====================

def registrar_madre(request):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "jefe_area", "admin"]:
        return redirect("/dashboard/")

    if request.method == "POST":
        rut = request.POST.get("rut")
        nombre = request.POST.get("nombre")
        edad = request.POST.get("edad")
        direccion = request.POST.get("direccion")

        if Madre.objects.filter(rut=rut).exists():
            return render(request, "madres_registrar.html", {
                "error": "❌ Ya existe una madre con ese RUT."
            })

        Madre.objects.create(
            rut=rut,
            nombre=nombre,
            edad=edad,
            direccion=direccion
        )
        return redirect("/madres/")

    return render(request, "madres_registrar.html")


def madre_editar(request, id):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "jefe_area", "admin"]:
        return redirect("/dashboard/")
        
    madre = get_object_or_404(Madre, id=id)

    if request.method == "POST":
        madre.nombre = request.POST.get("nombre")
        madre.edad = request.POST.get("edad")
        madre.direccion = request.POST.get("direccion")
        madre.save()
        return redirect("/madres/")

    return render(request, "madres_editar.html", {"madre": madre})


def madre_eliminar(request, id):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "jefe_area", "admin"]:
        return redirect("/dashboard/")
        
    madre = get_object_or_404(Madre, id=id)
    madre.delete()
    return redirect("/madres/")


# ==================== PARTOS CRUD ====================

def registrar_parto(request):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "jefe_area", "admin"]:
        return redirect("/dashboard/")

    madres = Madre.objects.all()

    if request.method == "POST":
        madre_id = request.POST.get("madre")
        fecha = request.POST.get("fecha_parto")
        tipo = request.POST.get("tipo_parto")
        obs = request.POST.get("observaciones", "")

        madre = get_object_or_404(Madre, id=madre_id)

        Parto.objects.create(
            madre=madre,
            fecha_parto=fecha,
            tipo_parto=tipo,
            observaciones=obs
        )
        return redirect("/partos/")

    return render(request, "partos_registrar.html", {"madres": madres})


def parto_editar(request, id):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "jefe_area", "admin"]:
        return redirect("/dashboard/")
        
    parto = get_object_or_404(Parto, id=id)

    if request.method == "POST":
        parto.tipo_parto = request.POST.get("tipo_parto")
        parto.observaciones = request.POST.get("observaciones", "")
        parto.save()
        return redirect("/partos/")

    return render(request, "partos_editar.html", {"parto": parto})


def parto_eliminar(request, id):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "jefe_area", "admin"]:
        return redirect("/dashboard/")
        
    parto = get_object_or_404(Parto, id=id)
    parto.delete()
    return redirect("/partos/")


# ==================== RN CRUD ====================

def rn_editar(request, id):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "medico", "jefe_area", "admin"]:
        return redirect("/dashboard/")
        
    rn = get_object_or_404(RecienNacido, id=id)

    if request.method == "POST":
        peso = float(request.POST.get("peso"))
        talla = float(request.POST.get("talla"))
        apgar = int(request.POST.get("apgar"))
        sexo = request.POST.get("sexo")

        if peso < 0.5 or peso > 6:
            error = "❌ El peso debe estar entre 0.5 y 6 kg."
        elif talla < 40 or talla > 60:
            error = "❌ La talla debe estar entre 40 y 60 cm."
        elif apgar < 0 or apgar > 10:
            error = "❌ APGAR debe estar entre 0 y 10."
        else:
            rn.peso = peso
            rn.talla = talla
            rn.apgar = apgar
            rn.sexo = sexo
            rn.save()
            return redirect("/rn/")

    # Cargar template según el rol
    rol = request.session.get("rol")
    
    if rol == "medico":
        return render(request, "rn_editar_medico.html", {"rn": rn})
    else:
        return render(request, "rn_editar.html", {"rn": rn})


def rn_eliminar(request, id):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["matrona", "jefe_area", "admin"]:
        return redirect("/dashboard/")
        
    rn = get_object_or_404(RecienNacido, id=id)
    rn.delete()
    return redirect("/rn/")


# ==================== ACTIVIDAD ====================

def actividad_view(request):
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    if request.session.get("rol") not in ["jefe_area", "admin"]:
        return redirect("/dashboard/")
        
    return render(request, "actividad.html")


# ============================================
# VISTAS JEFE DE ÁREA
# ============================================

def reportes_view(request):
    """Vista de reportes con gráficos y estadísticas"""
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    if rol not in ["jefe_area", "admin"]:
        return redirect("/dashboard/")
    
    # Obtener datos para reportes
    hoy = timezone.now()
    mes_actual = hoy.month
    anio_actual = hoy.year
    
    # Estadísticas generales
    total_madres = Madre.objects.count()
    total_partos = Parto.objects.count()
    total_rn = RecienNacido.objects.count()
    
    # Partos del mes actual
    partos_mes = Parto.objects.filter(
        fecha_parto__month=mes_actual,
        fecha_parto__year=anio_actual
    ).count()
    
    # Partos por tipo
    partos_por_tipo = list(Parto.objects.values('tipo_parto').annotate(
        total=Count('id')
    ))
    
    # RN por sexo
    rn_por_sexo = list(RecienNacido.objects.values('sexo').annotate(
        total=Count('id')
    ))
    
    # Últimos 6 meses de partos
    meses_anteriores = []
    partos_por_mes_list = []
    for i in range(6, 0, -1):
        fecha = hoy - timedelta(days=30*i)
        mes = fecha.month
        anio = fecha.year
        count = Parto.objects.filter(
            fecha_parto__month=mes,
            fecha_parto__year=anio
        ).count()
        meses_anteriores.append(fecha.strftime("%B"))
        partos_por_mes_list.append(count)
    
    context = {
        "rol": rol,
        "total_madres": total_madres,
        "total_partos": total_partos,
        "total_rn": total_rn,
        "partos_mes": partos_mes,
        "partos_por_tipo": json.dumps(partos_por_tipo),
        "rn_por_sexo": json.dumps(rn_por_sexo),
        "meses_anteriores": json.dumps(meses_anteriores),
        "partos_por_mes": json.dumps(partos_por_mes_list),
    }
    
    return render(request, "reportes.html", context)


def personal_view(request):
    """Vista de gestión de personal"""
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    if rol not in ["jefe_area", "admin"]:
        return redirect("/dashboard/")
    
    # Obtener todo el personal
    personal = Usuario.objects.all().order_by('rol', 'nombre')
    
    # Estadísticas por rol
    estadisticas_rol = Usuario.objects.values('rol').annotate(
        total=Count('id')
    )
    
    # Convertir a diccionario para facilitar acceso
    stats_dict = {item['rol']: item['total'] for item in estadisticas_rol}
    
    context = {
        "rol": rol,
        "personal": personal,
        "total_personal": personal.count(),
        "total_matronas": stats_dict.get('matrona', 0),
        "total_medicos": stats_dict.get('medico', 0),
        "total_jefes": stats_dict.get('jefe_area', 0),
        "total_admins": stats_dict.get('admin', 0),
        "puede_editar": True,
        "puede_eliminar": True,
    }
    
    return render(request, "personal.html", context)


def analisis_view(request):
    """Vista de análisis y KPIs"""
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    if rol not in ["jefe_area", "admin"]:
        return redirect("/dashboard/")
    
    hoy = timezone.now()
    
    # Análisis de tendencias
    edad_promedio = Madre.objects.aggregate(Avg('edad'))['edad__avg']
    
    # Tasa de cesáreas vs partos normales
    total_partos = Parto.objects.count()
    cesareas = Parto.objects.filter(tipo_parto='cesarea').count()
    normales = Parto.objects.filter(tipo_parto='normal').count()
    
    tasa_cesareas = (cesareas / total_partos * 100) if total_partos > 0 else 0
    tasa_normales = (normales / total_partos * 100) if total_partos > 0 else 0
    
    # Promedio de peso de RN
    peso_promedio = RecienNacido.objects.aggregate(Avg('peso'))['peso__avg']
    
    # RN con bajo peso (< 2500g)
    bajo_peso = RecienNacido.objects.filter(peso__lt=2500).count()
    
    # Partos de último mes
    mes_pasado = hoy - timedelta(days=30)
    partos_ultimo_mes = Parto.objects.filter(
        fecha_parto__gte=mes_pasado
    ).count()
    
    # Tendencia (comparar con mes anterior)
    dos_meses = hoy - timedelta(days=60)
    partos_mes_anterior = Parto.objects.filter(
        fecha_parto__gte=dos_meses,
        fecha_parto__lt=mes_pasado
    ).count()
    
    if partos_mes_anterior > 0:
        tendencia = ((partos_ultimo_mes - partos_mes_anterior) / partos_mes_anterior) * 100
    else:
        tendencia = 0
    
    context = {
        "rol": rol,
        "edad_promedio": round(edad_promedio, 1) if edad_promedio else 0,
        "tasa_cesareas": round(tasa_cesareas, 1),
        "tasa_normales": round(tasa_normales, 1),
        "peso_promedio": round(peso_promedio, 0) if peso_promedio else 0,
        "bajo_peso": bajo_peso,
        "partos_ultimo_mes": partos_ultimo_mes,
        "partos_mes_anterior": partos_mes_anterior,
        "tendencia": round(tendencia, 1),
        "total_partos": total_partos,
        "cesareas": cesareas,
        "normales": normales,
    }
    
    return render(request, "analisis.html", context)