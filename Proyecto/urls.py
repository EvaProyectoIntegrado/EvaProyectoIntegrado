from django.contrib import admin
from django.urls import path
from usuarios import views as web
from api import views as api

urlpatterns = [
    # FRONTEND (HTML)
    path("", web.dashboard, name="dashboard"),         # dashboard visible en "/"
    path("dashboard/", web.dashboard, name="dashboard_page"),  # dashboard visible en "/dashboard/"

    path("login/", web.login_view, name="login"),
    path("registrar/", web.register_view, name="registrar"),

    # Módulos HTML
    path("madres/", web.madres_view, name="madres"),
    path("partos/", web.partos_view, name="partos"),
    path("rn/", web.rn_view, name="rn"),
    path("usuarios/", web.usuarios_view, name="usuarios"),

    # API
    path("api/login/", api.login),
    path("api/registrar/", api.registrar_usuario),

    path("api/usuarios/", api.listar_usuarios),
    path("api/dashboard/", api.dashboard_datos),

    # API Madres
    path("api/madres/", api.listar_madres),
    path("api/madre/crear/", api.crear_madre),
    path("api/madre/<int:id>/", api.obtener_madre),
    path("api/madre/<int:id>/actualizar/", api.actualizar_madre),
    path("api/madre/<int:id>/eliminar/", api.eliminar_madre),

    # API Partos
    path("api/partos/", api.listar_partos),
    path("api/parto/crear/", api.crear_parto),
    path("api/parto/<int:id>/", api.obtener_parto),
    path("api/parto/<int:id>/actualizar/", api.actualizar_parto),
    path("api/parto/<int:id>/eliminar/", api.eliminar_parto),

    # API RN
    path("api/rn/", api.listar_rn),
    path("api/rn/crear/", api.crear_rn),
    path("api/rn/<int:id>/", api.obtener_rn),
    path("api/rn/<int:id>/actualizar/", api.actualizar_rn),
    path("api/rn/<int:id>/eliminar/", api.eliminar_rn),

    # PDF
    path("descargar-rem22/", api.descargar_rem22),

    # Admin
    path("admin/", admin.site.urls),
]

