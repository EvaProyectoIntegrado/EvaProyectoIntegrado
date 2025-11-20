from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from api import views as api

# -----------------------
#  VISTAS HTML
# -----------------------

def home(request):
    return render(request, "base.html")

def login_view(request):
    return render(request, "login.html")

def registrar_view(request):
    return render(request, "registrar.html")

def dashboard(request):
    return render(request, "dashboard.html")

def vista_madres(request):
    return render(request, "madres.html")

def vista_partos(request):
    return render(request, "partos.html")

def vista_rn(request):
    return render(request, "rn.html")


urlpatterns = [

    # HOME
    path("", home),

    # LOGIN & REGISTRO (VISUALES)
    path("login/", login_view),
    path("registrar/", registrar_view),

    # PANTALLAS PRINCIPALES
    path("dashboard/", dashboard),
    path("madres/", vista_madres),
    path("partos/", vista_partos),
    path("rn/", vista_rn),

    # PDF REM22
    path("descargar-rem22/", api.descargar_rem22),

    # =========================
    #         API
    # =========================

    # Usuarios
    path('api/registrar/', api.registrar_usuario),
    path('api/login/', api.login),

    # Madres
    path('api/madre/crear/', api.crear_madre),
    path('api/madres/', api.listar_madres),
    path('api/madre/<int:id>/', api.obtener_madre),
    path('api/madre/<int:id>/actualizar/', api.actualizar_madre),
    path('api/madre/<int:id>/eliminar/', api.eliminar_madre),

    # Partos
    path('api/parto/crear/', api.crear_parto),
    path('api/partos/', api.listar_partos),
    path('api/parto/<int:id>/', api.obtener_parto),
    path('api/parto/<int:id>/actualizar/', api.actualizar_parto),
    path('api/parto/<int:id>/eliminar/', api.eliminar_parto),

    # Recién nacidos
    path('api/rn/crear/', api.crear_rn),
    path('api/rn/', api.listar_rn),
    path('api/rn/<int:id>/', api.obtener_rn),
    path('api/rn/<int:id>/actualizar/', api.actualizar_rn),
    path('api/rn/<int:id>/eliminar/', api.eliminar_rn),

    # Reporte API
    path('api/reportes/rem22/', api.descargar_rem22),


    # ADMIN
    path("admin/", admin.site.urls),
]
