"""
URL configuration for ProyectoEcomerceapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.api import UserClienteAPI
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('EcomerceApp.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api/crear-usuario/', UserClienteAPI.as_view(), name='crear_usuario_api'),
    path('crear-usuario-form/', TemplateView.as_view(template_name='Crear_Usuario_Form.html'), name='crear_usuario_form'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


