"""
URL configuration for sge_core project.

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
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings # Importa as configurações do Django

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),  # URLs do app de autenticação
    path('dashboard/', include('dashboard.urls')),  # URLs do app de dashboard
    path('movimentacoes/', include('movimentacoes.urls')),  # URLs do app de movimentações
    path('estoque/', include('estoque.urls')),  # URLs do app de estoque
    path('produtos/', include('produtos.urls')),  # URLs do app de produtos
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)