from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from import_export.admin import ImportExportMixin
from user.models import User
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    
class ProvinciaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome']

class SectorAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'provincia']
    list_filter = ('provincia',)
    
class InstrumentoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'nome', 'stock', 'provincia', 'sector']
    list_filter = ('provincia', 'sector',)
    
class NecessidadeAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'provincia', 'sector', 'instrumento', 'ano', 'quantidade']
    list_filter = ('provincia', 'sector',)
    
class EntradaAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'data_entrada', 'fornecedor', 'quantidade', 'provincia','instrumento']
    list_filter = ('provincia',)
    
class LevantamentoDepositoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'data_levantamento', 'provincia', 'instrumento', 'quantidade']
    
class RequisicaoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'data_requisicao', 'provincia', 'instrumento', 'quantidade']
    
class AprovacaoAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['id', 'requisicao', 'tipo_aprovacao', 'comentario']

admin.site.register(User, UserAdmin)
admin.site.register(models.Provincia, ProvinciaAdmin)
admin.site.register(models.Sector, SectorAdmin)
admin.site.register(models.Instrumento, InstrumentoAdmin)
admin.site.register(models.Necessidade, NecessidadeAdmin)
admin.site.register(models.Entrada, EntradaAdmin)
admin.site.register(models.LevantamentoDeposito, LevantamentoDepositoAdmin)
admin.site.register(models.Requisicao, RequisicaoAdmin)
admin.site.register(models.Aprovacao, AprovacaoAdmin)
