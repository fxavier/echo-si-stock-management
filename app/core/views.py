from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Max, Min, Sum

from core.models import Provincia, Sector, Instrumento, Necessidade, Entrada, Requisicao, Aprovacao, ResumoInstrumento
from core.forms import InstrumentoForm, EntradaForm, SectorForm, NecessidadeForm

class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'stock_list'
    model = Instrumento
    paginate_by = 6
    
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['stock_manica'] = Instrumento.objects.filter(provincia=Provincia.objects.get(nome='Manica')).count() #.aggregate(Sum('stock'))['stock__sum']
        context['stock_sofala'] = Instrumento.objects.filter(provincia=Provincia.objects.get(nome='Sofala')).count() #.aggregate(Sum('stock'))['stock__sum']
        context['stock_tete']   = Instrumento.objects.filter(provincia=Provincia.objects.get(nome='Tete')).count() #.aggregate(Sum('stock'))['stock__sum']
        context['stock_niassa'] = Instrumento.objects.filter(provincia=Provincia.objects.get(nome='Niassa')).count() #.aggregate(Sum('stock'))['stock__sum']
        if context['stock_manica'] is None:
           context['stock_manica'] = 0
        if context['stock_sofala'] is None:
            context['stock_sofala'] = 0
        if context['stock_tete'] is None:
            context['stock_tete'] = 0
        if context['stock_niassa'] is None:
            context['stock_niassa'] = 0
        return context
    
    def get_queryset(self):
        return Instrumento.objects.all()
    
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = ResumoInstrumento.objects.all()
    #     qs = qs.select_related('entrada')
    #     qs = qs.select_related('necessidade')
    #     qs = qs.select_related('requisicao')
        
    #     return qs
    
class SectorListView(ListView):
    template_name = 'sector_list.html'
    context_object_name = 'sectores'
    model = Sector
    
class SectorCreateView(SuccessMessageMixin, CreateView):
    template_name = 'sector_create.html'
    form_class = SectorForm
    success_url = '/'
    success_message = 'Sector adicionado com sucesso'
    
    def form_valid(self, form):
        sector = form.save(commit=False)
        sector.save()
        return redirect(self.success_url)
    
    
class TodosInstrumentosListView(ListView):
    template_name = 'instrumento_list.html'
    context_object_name = 'instrumentos'
    model = Instrumento
    
    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     qs = qs.select_related('provincia')
    #     qs = qs.select_related('sector')
        
    #     return qs
    
    
class InstrumentoCreateView(SuccessMessageMixin, CreateView):
    template_name = 'instrumento_create.html'
    form_class = InstrumentoForm
    success_url = '/'
    success_message = 'Instrumento adicionado com sucesso'
    
    def form_valid(self, form):
        instrumento = form.save(commit=False)
        instrumento.save()
        return redirect(self.success_url)
    
   
class EntradasListView(ListView):
    template_name = 'entrada_list.html'
    context_object_name = 'entradas'
    model = Entrada
    
    def get_queryset(self):
        qs = Entrada.objects.all()
        return qs
    
class EntradaCreateView(SuccessMessageMixin, CreateView):
    template_name = 'entrada_create.html'
    form_class = EntradaForm
    success_url = '/'
    success_message = 'Movimento adicionado com sucesso'
    
    def form_valid(self, form):
        entrada = form.save(commit=False)
        entrada.save()
        return redirect(self.success_url)

def load_sectores(request):
    provincia_id = request.GET.get('provincia')
    sectores = Sector.objects.filter(provincia_id=provincia_id).order_by('nome')
    context = {'sectores': sectores}
    return render(request, 'sector_dropdown_list_options.html', context)

def load_instrumentos(request):
    sector_id = request.GET.get('sector')
    instrumentos = Instrumento.objects.filter(sector_id=sector_id).order_by('nome')
    context = {'instrumentos': instrumentos}
    return render(request, 'instrumento_dropdown_list_options.html', context)

class NecessidadeLisView(ListView):
    template_name = 'necessidade_list.html'
    context_object_name = 'necessidades'
    model = Necessidade
    
class NecessidadeCreateView(SuccessMessageMixin, CreateView):
    template_name = 'necessidade_create.html'
    form_class = NecessidadeForm
    success_url = '/'
    success_message = 'Necessidade adicionada com sucesso'
    
    def form_valid(self, form):
        necessidade = form.save(commit=False)
        necessidade.save()
        return redirect(self.success_url)
    
class ResumoInstrumentosListView(ListView):
    template_name = 'resumo_instrumentos.html'
    context_object_name = 'resumo_instrumentos'
    
    def get_queryset(self):
        qs = Instrumento.objects.all().order_by('provincia')
        return qs