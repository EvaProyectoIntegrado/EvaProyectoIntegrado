from django.contrib import admin
from django.urls import path
from usuarios import views as web
from api import views as api

urlpatterns = [
    # FRONTEND
    path("", web.dashboard, name="dashboard"),
    path("dashboard/", web.dashboard, name="dashboard_page"),

    path("login/", web.login_view, name="login"),
    path("registrar/", web.register_view, name="registrar"),

    # -----------------------
    # CRUD MADRES
    # -----------------------
    path("madres/", web.madres_list, name="madres"),
    path("madres/registrar/", web.registrar_madre, name="registrar_madre"),
    path("madres/editar/<int:id>/", web.madre_editar, name="madre_editar"),
    path("madres/eliminar/<int:id>/", web.madre_eliminar, name="madre_eliminar"),

    # -----------------------
    # CRUD PARTOS
    # -----------------------
    path("partos/", web.partos_list, name="partos"),
    path("partos/registrar/", web.registrar_parto, name="registrar_parto"),
    path("partos/editar/<int:id>/", web.parto_editar, name="parto_editar"),
    path("partos/eliminar/<int:id>/", web.parto_eliminar, name="parto_eliminar"),

    # -----------------------
    # CRUD RN
    # -----------------------
    path("rn/", web.rn_view, name="rn"),
    path("rn/editar/<int:id>/", web.rn_editar, name="rn_editar"),
    path("rn/eliminar/<int:id>/", web.rn_eliminar, name="rn_eliminar"),

    # -----------------------
    # USUARIOS
    # -----------------------
    path("usuarios/", web.usuarios_view, name="usuarios"),

    # -----------------------
    # PDF
    # -----------------------
    path("descargar-rem22/", api.descargar_rem22, name="descargar_rem22"),

    # -----------------------
    # URLs para Jefe de Área
    # -----------------------
    path('reportes/', web.reportes_view, name='reportes'),
    path('reportes/exportar-pdf/', web.exportar_pdf_reportes, name='exportar_pdf_reportes'),  # ← AGREGADO
    path('personal/', web.personal_view, name='personal'),
    path('personal/crear/', web.crear_personal, name='crear_personal'),
    path('personal/editar/<int:id>/', web.editar_personal, name='editar_personal'),
    path('personal/eliminar/<int:id>/', web.eliminar_personal, name='eliminar_personal'),
    path('analisis/', web.analisis_view, name='analisis'),

    # -----------------------
    # URLs para Administrador
    # -----------------------
    path('admin/usuarios/', web.admin_usuarios_view, name='admin_usuarios'),
    path('admin/areas/', web.admin_areas_view, name='admin_areas'),
    path('admin/reportes/', web.admin_reportes_view, name='admin_reportes'),
    path('admin/procesos/', web.admin_procesos_view, name='admin_procesos'),

    # -----------------------
    # API REST (NO TOCAR)
    # -----------------------
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

    # Admin Django
    path("admin/django/", admin.site.urls),
    
]