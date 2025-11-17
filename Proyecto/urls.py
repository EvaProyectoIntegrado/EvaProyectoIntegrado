"""
URL configuration for Proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api import views     # <---- IMPORTACIÓN CORRECTA

urlpatterns = [
    path('admin/', admin.site.urls),

    # USUARIOS
    path('api/registrar/', views.registrar_usuario),
    path('api/login/', views.login),

    # MADRE
    path('api/madre/crear/', views.crear_madre),
    path('api/madres/', views.listar_madres),
    path('api/madre/<int:id>/', views.obtener_madre),
    path('api/madre/<int:id>/actualizar/', views.actualizar_madre),
    path('api/madre/<int:id>/eliminar/', views.eliminar_madre),

    # PARTO
    path('api/parto/crear/', views.crear_parto),
    path('api/partos/', views.listar_partos),
    path('api/parto/<int:id>/', views.obtener_parto),
    path('api/parto/<int:id>/actualizar/', views.actualizar_parto),
    path('api/parto/<int:id>/eliminar/', views.eliminar_parto),

    # RN
    path('api/rn/crear/', views.crear_rn),
    path('api/rn/', views.listar_rn),
    path('api/rn/<int:id>/', views.obtener_rn),
    path('api/rn/<int:id>/actualizar/', views.actualizar_rn),
    path('api/rn/<int:id>/eliminar/', views.eliminar_rn),

    # INFORME REM22
    path('api/reportes/rem22/', views.generar_informe_rem),
]
