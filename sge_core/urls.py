from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.conf import settings # Importa as configurações do Django
from django.views.generic.base import RedirectView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls), # URLs do admin
    path('', login_required(RedirectView.as_view(url='/dashboard/', permanent=False)), name='dashboard'),  # Redireciona para o dashboard
    path('authentication/', include('authentication.urls')),  # URLs do app de autenticação
    path('dashboard/', include('dashboard.urls')),  # URLs do app de dashboard
    path('movimentacoes/', include('movimentacoes.urls')),  # URLs do app de movimentações
    path('estoque/', include('estoque.urls')),  # URLs do app de estoque
    path('produtos/', include('produtos.urls')),  # URLs do app de produtos
    path('clientes/', include('clientes.urls')),  # URLs do app de clientes
    path('funcionarios/', include('funcionarios.urls')),  # URLs do app de funcionários
    path('fornecedores/', include('fornecedores.urls')),  # URLs do app de fornecedores
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)