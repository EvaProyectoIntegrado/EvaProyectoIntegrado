from django.contrib import admin
from django.urls import path
from usuarios import views as web  # vistas para HTML
from api import views as api       # vistas para API
from usuarios.views import usuarios_view

urlpatterns = [
    # FRONTEND (HTML)
    path("", web.dashboard, name="dashboard"),
    path("login/", web.login_view, name="login"),
    path("registrar/", web.register_view, name="registrar"),

    # estas son las que TE FALTAN 👇👇👇
    path("madres/", web.madres_view, name="madres"),
    path("partos/", web.partos_view, name="partos"),
    path("rn/", web.rn_view, name="rn"),
    path("usuarios/", web.usuarios_view, name="usuarios"),

    # BACKEND API (JSON)
    path("api/login/", api.login),
    path("api/registrar/", api.registrar_usuario),
    path("api/usuarios/", api.listar_usuarios),
    path("api/dashboard/", api.dashboard_datos),

    path("api/madres/", api.listar_madres),
    path("api/madre/crear/", api.crear_madre),
    path("api/madre/<int:id>/", api.obtener_madre),
    path("api/madre/<int:id>/actualizar/", api.actualizar_madre),
    path("api/madre/<int:id>/eliminar/", api.eliminar_madre),

    path("api/partos/", api.listar_partos),
    path("api/parto/crear/", api.crear_parto),
    path("api/parto/<int:id>/", api.obtener_parto),
    path("api/parto/<int:id>/actualizar/", api.actualizar_parto),
    path("api/parto/<int:id>/eliminar/", api.eliminar_parto),

    path("api/rn/", api.listar_rn),
    path("api/rn/crear/", api.crear_rn),
    path("api/rn/<int:id>/", api.obtener_rn),
    path("api/rn/<int:id>/actualizar/", api.actualizar_rn),
    path("api/rn/<int:id>/eliminar/", api.eliminar_rn),

    path("descargar-rem22/", api.descargar_rem22),

    path("admin/", admin.site.urls),
]
