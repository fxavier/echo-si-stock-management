from django import forms
from django.utils.translation import ugettext as _

from core.models import Instrumento, Provincia, Sector, Entrada, Necessidade


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ('provincia', 'nome',)
        
        label = {
            'provincia': _('Provincia'),
            'nome': _('Nome'),
        }

class InstrumentoForm(forms.ModelForm):
    class Meta:
        model = Instrumento
        fields = ('provincia', 'sector', 'nome', 'stock')
        
        label = {
            'provincia': _('Provincia'),
            'sector': _('Sector'),
            'nome': _('Nome'),
            'stock': _('Stock'),
        }
        
        
class EntradaForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ('data_entrada', 'provincia','fornecedor', 'sector', 'instrumento','quantidade')
        
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
        self.fields['sector'].queryset =Sector.objects.none()
        
        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                self.fields['sector'].queryset = Sector.objects.filter(provincia_id=provincia_id).order_by('nome')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['provincia'].queryset = self.instance.provincia.sector_set.order_by('nome')
            
        
        if 'sector' in self.data: 
            try:
                sector_id = int(self.data.get('sector'))
                self.fields['instrumento'].queryset = Instrumento.objects.filter(sector_id=sector_id).order_by('nome')
            except(ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['sector'].queryset = self.instance.sector.instrumento_set.order_by('nome')
       
            
            
class NecessidadeForm(forms.ModelForm):
    class Meta:
        model = Necessidade
        fields = ('provincia', 'sector', 'ano', 'instrumento', 'quantidade')
        
        labels = {
            'provincia': _('Provincia'),
            'sector': _('Sector'),
            'ano': _('Ano'),
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
        