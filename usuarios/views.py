# REEMPLAZA TODO TU ARCHIVO views.py CON ESTE CÓDIGO CORREGIDO
from django.http import HttpResponse  # ← AGREGAR ESTA LÍNEA
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
    """
    Vista de lista de usuarios del sistema.
    
    Permisos:
        - Jefe de Área (solo visualización)
        - Administrador (visualización completa)
        
    Returns:
        HttpResponse: Template usuarios.html con lista de usuarios
    """
    if not request.session.get("usuario_id"):
        return redirect("/login/")
        
    rol = request.session.get("rol")
    
    if rol not in ["jefe_area", "admin"]:
        return redirect("/dashboard/")
    
    # Obtener todos los usuarios ordenados por nombre
    usuarios = Usuario.objects.all().order_by('nombre')
    
    # Estadísticas por rol
    total_usuarios = usuarios.count()
    total_matronas = Usuario.objects.filter(rol='matrona').count()
    total_medicos = Usuario.objects.filter(rol='medico').count()
    total_jefes = Usuario.objects.filter(rol='jefe_area').count()
    total_admins = Usuario.objects.filter(rol='admin').count()
    
    context = {
        "rol": rol,
        "usuarios": usuarios,
        "total_usuarios": total_usuarios,
        "total_matronas": total_matronas,
        "total_medicos": total_medicos,
        "total_jefes": total_jefes,
        "total_admins": total_admins,
    }
    
    return render(request, "usuarios.html", context)


# ==================== LOGIN Y REGISTRO ====================

def login_view(request):
    return render(request, "login.html")


def register_view(request):
    """
    Vista de registro de nuevos usuarios.
    
    Permisos:
        - Solo Administrador
        
    Restricciones:
        - Requiere rol 'admin'
        - Redirecciona a dashboard si no tiene permisos
        
    Returns:
        HttpResponse: Template de registro o redirección
    """
    # Solo admin puede registrar usuarios
    if request.session.get("rol") != "admin":
        return redirect("/dashboard/")
    
    return render(request, "registrar.html")


# ==================== DASHBOARD ====================

def dashboard(request):
    """
    Vista principal del dashboard con estadísticas y gráficos.
    
    Muestra diferentes dashboards según el rol del usuario.
    """
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    # Obtener estadísticas generales
    hoy = timezone.now()
    mes_actual = hoy.month
    anio_actual = hoy.year
    
    total_madres = Madre.objects.count()
    total_partos = Parto.objects.count()
    total_rn = RecienNacido.objects.count()
    partos_mes = Parto.objects.filter(
        fecha_parto__month=mes_actual,
        fecha_parto__year=anio_actual
    ).count()
    
    # Datos para gráficos (solo si hay partos)
    if total_partos > 0:
        # Partos por tipo
        cesareas = Parto.objects.filter(tipo_parto='cesarea').count()
        normales = Parto.objects.filter(tipo_parto='normal').count()
        inducidos = Parto.objects.filter(tipo_parto='inducido').count()
        
        # RN por sexo
        rn_masculino = RecienNacido.objects.filter(sexo='M').count()
        rn_femenino = RecienNacido.objects.filter(sexo='F').count()
        
        # Últimos 6 meses
        meses_labels = []
        partos_por_mes_datos = []
        
        for i in range(6, 0, -1):
            fecha = hoy - timedelta(days=30*i)
            mes = fecha.month
            anio = fecha.year
            count = Parto.objects.filter(
                fecha_parto__month=mes,
                fecha_parto__year=anio
            ).count()
            meses_labels.append(fecha.strftime("%B"))
            partos_por_mes_datos.append(count)
    else:
        cesareas = normales = inducidos = 0
        rn_masculino = rn_femenino = 0
        meses_labels = ['Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov']
        partos_por_mes_datos = [0, 0, 0, 0, 0, 0]
    
    context = {
        'total_madres': total_madres,
        'total_partos': total_partos,
        'total_rn': total_rn,
        'partos_mes': partos_mes,
        'cesareas': cesareas,
        'normales': normales,
        'inducidos': inducidos,
        'rn_masculino': rn_masculino,
        'rn_femenino': rn_femenino,
        'meses_labels': json.dumps(meses_labels),
        'partos_por_mes_datos': json.dumps(partos_por_mes_datos),
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

def crear_personal(request):
    """
    Vista para crear nuevo personal desde el módulo de gestión.
    
    Permisos:
        - Solo Administrador
        
    Args:
        request (HttpRequest): Petición con datos del formulario
        
    Returns:
        HttpResponse: Renderiza personal.html con error o redirecciona
    """
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    
    # Solo admin puede crear personal
    if rol != "admin":
        return redirect("/dashboard/")
    
    error = None
    
    if request.method == "POST":
        rut = request.POST.get("rut")
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        password = request.POST.get("password")
        rol_nuevo = request.POST.get("rol")
        
        # Validaciones
        if not all([rut, nombre, email, password, rol_nuevo]):
            error = "❌ Todos los campos son obligatorios"
        elif Usuario.objects.filter(email=email).exists():
            error = "❌ Ya existe un usuario con ese email"
        elif Usuario.objects.filter(rut=rut).exists():
            error = "❌ Ya existe un usuario con ese RUT"
        else:
            # Crear usuario
            from django.contrib.auth.hashers import make_password
            Usuario.objects.create(
                rut=rut,
                nombre=nombre,
                email=email,
                contraseña=make_password(password),
                rol=rol_nuevo
            )
            return redirect("/personal/")
    
    context = {
        "rol": rol,
        "error": error,
    }
    
    return render(request, "personal.html", context)

def editar_personal(request, id):
    """
    Vista para editar personal existente.
    
    Permisos:
        - Solo Administrador
    """
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    
    # Solo admin puede editar
    if rol != "admin":
        return redirect("/dashboard/")
    
    persona = get_object_or_404(Usuario, id=id)
    error = None
    
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        email = request.POST.get("email")
        rol_nuevo = request.POST.get("rol")
        
        # Validar que el email no esté en uso por otro usuario
        if Usuario.objects.filter(email=email).exclude(id=id).exists():
            error = "❌ Ya existe otro usuario con ese email"
        else:
            persona.nombre = nombre
            persona.email = email
            persona.rol = rol_nuevo
            persona.save()
            return redirect("/personal/")
    
    context = {
        "rol": rol,
        "persona": persona,
        "error": error,
    }
    
    return render(request, "personal_editar.html", context)


def eliminar_personal(request, id):
    """
    Vista para eliminar personal del sistema.
    
    Permisos:
        - Solo Administrador
    """
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    
    # Solo admin puede eliminar
    if rol != "admin":
        return redirect("/dashboard/")
    
    persona = get_object_or_404(Usuario, id=id)
    persona.delete()
    
    return redirect("/personal/")

# ============================================
# VISTAS ADMINISTRADOR
# ============================================

def admin_usuarios_view(request):
    """Vista de gestión total de usuarios para admin"""
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    if rol != "admin":
        return redirect("/dashboard/")
    
    usuarios = Usuario.objects.all().order_by('-id')
    
    # Estadísticas detalladas
    total_usuarios = usuarios.count()
    usuarios_activos = total_usuarios  # Puedes agregar campo 'activo' después
    matronas = Usuario.objects.filter(rol='matrona').count()
    medicos = Usuario.objects.filter(rol='medico').count()
    jefes = Usuario.objects.filter(rol='jefe_area').count()
    admins = Usuario.objects.filter(rol='admin').count()
    
    context = {
        "rol": rol,
        "usuarios": usuarios,
        "total_usuarios": total_usuarios,
        "usuarios_activos": usuarios_activos,
        "matronas": matronas,
        "medicos": medicos,
        "jefes": jefes,
        "admins": admins,
    }
    
    return render(request, "admin_usuarios.html", context)


def admin_areas_view(request):
    """Vista de áreas registradas"""
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    if rol != "admin":
        return redirect("/dashboard/")
    
    # Estadísticas por área
    total_madres = Madre.objects.count()
    total_partos = Parto.objects.count()
    total_rn = RecienNacido.objects.count()
    
    # Áreas ficticias (puedes crear un modelo después)
    areas = [
        {"nombre": "Maternidad", "pacientes": total_madres, "activa": True},
        {"nombre": "Sala de Partos", "pacientes": total_partos, "activa": True},
        {"nombre": "Neonatología", "pacientes": total_rn, "activa": True},
    ]
    
    context = {
        "rol": rol,
        "areas": areas,
        "total_areas": len(areas),
        "total_madres": total_madres,
        "total_partos": total_partos,
        "total_rn": total_rn,
    }
    
    return render(request, "admin_areas.html", context)


def admin_reportes_view(request):
    """Vista de reportes mensuales"""
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    if rol != "admin":
        return redirect("/dashboard/")
    
    hoy = timezone.now()
    mes_actual = hoy.month
    anio_actual = hoy.year
    
    # Reportes del mes
    partos_mes = Parto.objects.filter(
        fecha_parto__month=mes_actual,
        fecha_parto__year=anio_actual
    ).count()
    
    madres_mes = Madre.objects.filter(
        id__in=Parto.objects.filter(
            fecha_parto__month=mes_actual,
            fecha_parto__year=anio_actual
        ).values_list('madre_id', flat=True)
    ).count()
    
    rn_mes = RecienNacido.objects.filter(
        parto__fecha_parto__month=mes_actual,
        parto__fecha_parto__year=anio_actual
    ).count()
    
    context = {
        "rol": rol,
        "mes_nombre": hoy.strftime("%B %Y"),
        "partos_mes": partos_mes,
        "madres_mes": madres_mes,
        "rn_mes": rn_mes,
        "total_reportes": partos_mes + madres_mes + rn_mes,
    }
    
    return render(request, "admin_reportes.html", context)


def admin_procesos_view(request):
    """Vista de procesos activos del sistema"""
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    if rol != "admin":
        return redirect("/dashboard/")
    
    # Procesos activos simulados
    procesos = [
        {"nombre": "Sistema de Registro", "estado": "Activo", "uso": "85%"},
        {"nombre": "Base de Datos", "estado": "Activo", "uso": "60%"},
        {"nombre": "Generación de PDFs", "estado": "Activo", "uso": "40%"},
        {"nombre": "Sistema de Sesiones", "estado": "Activo", "uso": "70%"},
    ]
    
    context = {
        "rol": rol,
        "procesos": procesos,
        "total_procesos": len(procesos),
        "procesos_activos": len([p for p in procesos if p['estado'] == 'Activo']),
    }
    
    return render(request, "admin_procesos.html", context)

# ============================================
# EXPORTAR PDF DE REPORTES
# ============================================
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from io import BytesIO

def exportar_pdf_reportes(request):
    """Genera PDF completo con estadísticas y reportes"""
    if not request.session.get("usuario_id"):
        return redirect("/login/")
    
    rol = request.session.get("rol")
    if rol not in ["jefe_area", "admin"]:
        return redirect("/dashboard/")
    
    # Crear el PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Reporte_Maternidad_{timezone.now().strftime("%Y%m%d_%H%M%S")}.pdf"'
    
    # Crear el documento
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container para los elementos
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#0066CC'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#111827'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    # Título principal
    elements.append(Paragraph("REPORTE DE ESTADISTICAS - SISTEMA MATERNIDAD", title_style))
    elements.append(Paragraph("Sistema de Gestion Maternidad", styles['Normal']))
    elements.append(Paragraph(f"Generado: {timezone.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
    elements.append(Spacer(1, 0.5*inch))
    
    # Obtener datos
    hoy = timezone.now()
    mes_actual = hoy.month
    anio_actual = hoy.year
    
    total_madres = Madre.objects.count()
    total_partos = Parto.objects.count()
    total_rn = RecienNacido.objects.count()
    partos_mes = Parto.objects.filter(
        fecha_parto__month=mes_actual,
        fecha_parto__year=anio_actual
    ).count()
    
    # SECCIÓN 1: Resumen Ejecutivo
    elements.append(Paragraph("1. RESUMEN EJECUTIVO", heading_style))
    
    data_resumen = [
        ['Indicador', 'Total'],
        ['Madres Registradas', str(total_madres)],
        ['Partos Totales', str(total_partos)],
        ['Recien Nacidos', str(total_rn)],
        ['Partos Este Mes', str(partos_mes)],
    ]
    
    table_resumen = Table(data_resumen, colWidths=[4*inch, 2*inch])
    table_resumen.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0066CC')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table_resumen)
    elements.append(Spacer(1, 0.3*inch))
    
    # SECCIÓN 2: Partos por Tipo
    elements.append(Paragraph("2. PARTOS POR TIPO", heading_style))
    
    partos_por_tipo = Parto.objects.values('tipo_parto').annotate(total=Count('id'))
    
    data_tipo = [['Tipo de Parto', 'Cantidad', 'Porcentaje']]
    for item in partos_por_tipo:
        porcentaje = (item['total'] / total_partos * 100) if total_partos > 0 else 0
        data_tipo.append([
            item['tipo_parto'].capitalize(),
            str(item['total']),
            f"{porcentaje:.1f}%"
        ])
    
    table_tipo = Table(data_tipo, colWidths=[2.5*inch, 2*inch, 1.5*inch])
    table_tipo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table_tipo)
    elements.append(Spacer(1, 0.3*inch))
    
    # SECCIÓN 3: Recién Nacidos por Sexo
    elements.append(Paragraph("3. RECIEN NACIDOS POR SEXO", heading_style))
    
    rn_por_sexo = RecienNacido.objects.values('sexo').annotate(total=Count('id'))
    
    data_sexo = [['Sexo', 'Cantidad', 'Porcentaje']]
    for item in rn_por_sexo:
        porcentaje = (item['total'] / total_rn * 100) if total_rn > 0 else 0
        data_sexo.append([
            item['sexo'],
            str(item['total']),
            f"{porcentaje:.1f}%"
        ])
    
    table_sexo = Table(data_sexo, colWidths=[2.5*inch, 2*inch, 1.5*inch])
    table_sexo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B5CF6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table_sexo)
    elements.append(Spacer(1, 0.3*inch))
    
    # SECCIÓN 4: Tendencia Mensual (últimos 6 meses)
    elements.append(Paragraph("4. TENDENCIA ULTIMOS 6 MESES", heading_style))
    
    data_tendencia = [['Mes', 'Cantidad de Partos']]
    
    for i in range(6, 0, -1):
        fecha = hoy - timedelta(days=30*i)
        mes = fecha.month
        anio = fecha.year
        count = Parto.objects.filter(
            fecha_parto__month=mes,
            fecha_parto__year=anio
        ).count()
        mes_nombre = fecha.strftime("%B %Y")
        data_tendencia.append([mes_nombre, str(count)])
    
    table_tendencia = Table(data_tendencia, colWidths=[3.5*inch, 2.5*inch])
    table_tendencia.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F59E0B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    elements.append(table_tendencia)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    elements.append(Paragraph("_______________________________________________", styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph("Sistema de Gestion Maternidad - 2025", styles['Normal']))
    
    # Construir PDF
    doc.build(elements)
    
    # Obtener el valor del buffer
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    
    return response

