from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.utils.translation import ugettext as _

from core.models import Instrumento, Provincia, Sector, Entrada, Requisicao, Aprovacao


class DateInput(forms.DateInput):
    input_type = 'date'

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ('nome',)
        
        label = {
            'nome': _('Nome'),
        }

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumento
        fields = ('provincia','sector', 'nome', 'ano', 'quantidade_necessaria', 'stock')
        
        label = {
            'provincia': _('Provincia'),
            'sector': _('Sector'),
            'nome': _('Nome'),
            'stock': _('Stock'),
            'ano': _('Ano'),
            'quantidade_necessaria': _('Necessidade')
         
        }
        
        
class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ('data_entrada', 'provincia','fornecedor', 'sector', 'instrumento','quantidade')
        
        widgets = {
            'data_entrada': DatePickerInput(),
        }
        
        labels = {
            'provincia': _('Provincia'),
            'fornecedor': _('Fornecedor'),
            'sector': _('Sector'),
            'data_entrada': _('Data de Entrada'),
            'instrumento': _('Instrumento'),
            'quantidade': _('Quantidade'),
            
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instrumento'].queryset = Instrumento.objects.none()
                    
        
        if 'sector' in self.data: 
            try:
                sector_id = int(self.data.get('sector'))
                self.fields['instrumento'].queryset = Instrumento.objects.filter(sector_id=sector_id).order_by('nome')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sector'].queryset = self.instance.sector.instrumento_set.order_by('nome')
       
            
                  
class RequisicaoForm(forms.ModelForm):
    class Meta:
        model = Requisicao
        fields = ('data_requisicao', 'provincia', 'sector', 'instrumento', 'quantidade')
        
        labels = {
            'data_requisicao': _('Data de Requisicao'),
            'provincia': _('Provincia'),
            'sector': _('Sector'),
            'instrumento': _('Instrumento'),
            'quantidade': _('Quantidade')
        }
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instrumento'].queryset = Instrumento.objects.none()
        
        if 'sector' in self.data: 
            try:
                sector_id = int(self.data.get('sector'))
                self.fields['instrumento'].queryset = Instrumento.objects.filter(sector_id=sector_id).order_by('nome')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sector'].queryset = self.instance.sector.instrumento_set.order_by('nome')
        
        
class AprovacaoForm(forms.ModelForm):
    
    class Meta:
        model = Aprovacao
        fields = ('requisicao','tipo_aprovacao', 'comentario')
        
        label = {
            'requisicao': _('Requisicao'),
            'tipo_aprovacao': _('Tipo Aprovacao'),
            'comentario': _('Comentario'),
                   
        }