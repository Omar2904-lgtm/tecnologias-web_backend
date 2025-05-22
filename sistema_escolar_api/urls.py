"""point_experts_api URL Configuration
# ... (docstring) ...
"""
from django.contrib import admin
from django.urls import path, include # Solo una vez path, include
from rest_framework.routers import DefaultRouter

# Importaciones de vistas desde el views.py de la app/proyecto
from sistema_escolar_api.views import bootstrap
from sistema_escolar_api.views import users
from sistema_escolar_api.views import alumnos
from sistema_escolar_api.views import maestros
from sistema_escolar_api.views import auth
from sistema_escolar_api.views import EventoViewSet # Cambiado de '.views' a 'sistema_escolar_api.views' para consistencia

router_eventos = DefaultRouter()
router_eventos.register(r'eventos', EventoViewSet, basename='evento')

urlpatterns = [
    #Version
    path('bootstrap/version', bootstrap.VersionView.as_view()),
    #Admin
    path('admin/', users.AdminView.as_view()), # Considera renombrar este 'admin/' si usas el admin de Django
                                               # Por ejemplo: path('django-admin-site/', admin.site.urls),
    path('lista-admins/', users.AdminAll.as_view()),
    path('admins-edit/', users.AdminViewEdit.as_view()),
    #Alumnos
    path('alumnos/', alumnos.AlumnosView.as_view()),
    path('lista-alumnos/', alumnos.AlumnosAll.as_view()),
    path('alumnos-edit/', alumnos.AlumnosViewEdit.as_view()),
    #Maestros 
    path('maestros/', maestros.MaestrosView.as_view()),
    path('lista-maestros/', maestros.MaestrosAll.as_view()),
    path('maestros-edit/', maestros.MaestrosViewEdit.as_view(), name='maestros-edit'),
    #Auth
    path('token/', auth.CustomAuthToken.as_view()),
    path('logout/', auth.Logout.as_view()),
    #Eventos API
    path('api/', include(router_eventos.urls)),
]