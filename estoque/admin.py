from django import forms
from django.contrib import admin
from django.http import HttpResponse
import csv
from openpyxl import Workbook
from .models import MovimentacaoEstoque
from django.contrib.auth.models import Permission, Group
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType

# Formulário para exportação personalizada
class ExportacaoPersonalizadaForm(forms.Form):
    colunas = forms.MultipleChoiceField(
        choices=[
            ('id', 'ID'),
            ('produto', 'Produto'),
            ('tipo', 'Tipo'),
            ('quantidade', 'Quantidade'),
            ('data_movimentacao', 'Data Movimentação'),
            ('observacoes', 'Observações')
        ],
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Colunas para exportação"
    )

# Register your models here.

# MovimentacaoEstoque

# Decorator para verificar permissões de forma consistente
def check_permission(permission):
    def decorator(func):
        @method_decorator(permission_required(permission, raise_exception=True))
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Atualizar as ações para usar o decorator
@check_permission('estoque.can_export_data')
@admin.action(description='Exportar para CSV')
def exportar_para_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="movimentacao_estoque.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Produto', 'Tipo', 'Quantidade', 'Data Movimentacao', 'Observacoes'])
    for movimentacao in queryset:
        writer.writerow([movimentacao.id, movimentacao.produto.nome, movimentacao.tipo, movimentacao.quantidade, movimentacao.data_movimentacao, movimentacao.observacoes])
    return response

@check_permission('estoque.can_export_data')
@admin.action(description='Exportar para Excel')
def exportar_para_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="movimentacao_estoque.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Movimentações"

    # Cabeçalhos
    ws.append(['ID', 'Produto', 'Tipo', 'Quantidade', 'Data Movimentacao', 'Observacoes'])

    # Dados
    for movimentacao in queryset:
        ws.append([
            movimentacao.id,
            movimentacao.produto.nome,
            movimentacao.tipo,
            movimentacao.quantidade,
            movimentacao.data_movimentacao,
            movimentacao.observacoes
        ])

    wb.save(response)
    return response

@check_permission('estoque.can_export_data')
@admin.action(description='Exportar para CSV (Personalizado)')
def exportar_para_csv_personalizado(modeladmin, request, queryset):
    form = ExportacaoPersonalizadaForm(request.POST or None)
    if 'apply' in request.POST and form.is_valid():
        colunas_selecionadas = form.cleaned_data['colunas']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="movimentacao_estoque_personalizado.csv"'
        writer = csv.writer(response)
        writer.writerow(colunas_selecionadas)
        for movimentacao in queryset:
            writer.writerow([getattr(movimentacao, coluna) for coluna in colunas_selecionadas])
        return response

    return admin.helpers.ActionFormResponse(
        request,
        form,
        title="Exportação Personalizada para CSV",
        description="Selecione as colunas que deseja exportar."
    )

@admin.register(MovimentacaoEstoque)
class MovimentacaoEstoqueAdmin(admin.ModelAdmin):
    list_display = ['produto', 'tipo', 'quantidade', 'data_movimentacao', 'observacoes']
    search_fields = ['produto__nome', 'tipo', 'quantidade', 'data_movimentacao', 'observacoes']
    list_filter = ['tipo']
    ordering = ['-data_movimentacao']
    list_per_page = 20
    actions = ['exportar_para_csv', 'exportar_para_excel', 'exportar_para_csv_personalizado']
    list_display_links = ['produto', 'data_movimentacao']
    list_editable = ['tipo', 'quantidade', 'observacoes']

    # Adicionar opção de alterar a paginação dinamicamente
    def get_changelist(self, request, **kwargs):
        from django.contrib.admin.views.main import ChangeList

        class CustomChangeList(ChangeList):
            def get_results(self, *args, **kwargs):
                self.list_per_page = int(request.GET.get('list_per_page', self.list_per_page))
                super().get_results(*args, **kwargs)

        return CustomChangeList

# Função para configurar grupos e permissões
def configurar_grupos_e_permissoes():
    # Criar ou obter o grupo "Gerente de Estoque"
    gerente_estoque, created = Group.objects.get_or_create(name="Gerente de Estoque")

    # Obter o ContentType do modelo MovimentacaoEstoque
    content_type = ContentType.objects.get_for_model(MovimentacaoEstoque)

    # Criar permissões específicas para o modelo
    permissoes = [
        ("can_add_movimentacao", "Pode adicionar movimentação"),
        ("can_change_movimentacao", "Pode alterar movimentação"),
        ("can_delete_movimentacao", "Pode deletar movimentação"),
        ("can_view_movimentacao", "Pode visualizar movimentação"),
    ]

    for codename, nome in permissoes:
        permissao, created = Permission.objects.get_or_create(
            codename=codename,
            name=nome,
            content_type=content_type
        )
        gerente_estoque.permissions.add(permissao)

    print("Grupos e permissões configurados com sucesso!")

# Chamar a função ao iniciar o sistema
configurar_grupos_e_permissoes()