from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, View, DetailView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Max, Min, Sum

from core.models import Provincia, Sector, Instrumento, Entrada, Requisicao, Aprovacao, Resumo
from core.forms import InstrumentoForm, EntradaForm, SectorForm, RequisicaoForm, AprovacaoForm

class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'stock_list'
    model = Instrumento
    paginate_by = 6
    
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
       # context['stock_manica'] = Instrumento.objects.filter(provincia=Provincia.objects.get(nome='Manica')).count() #.aggregate(Sum('stock'))['stock__sum']
       # context['stock_sofala'] = Instrumento.objects.filter(provincia=Provincia.objects.get(nome='Sofala')).count() #.aggregate(Sum('stock'))['stock__sum']
       # context['stock_tete']   = Instrumento.objects.filter(provincia=Provincia.objects.get(nome='Tete')).count() #.aggregate(Sum('stock'))['stock__sum']
        # context['stock_niassa'] = Instrumento.objects.filter(provincia=Provincia.objects.get(nome='Niassa')).count() #.aggregate(Sum('stock'))['stock__sum']
        # if context['stock_manica'] is None:
        #    context['stock_manica'] = 0
        # if context['stock_sofala'] is None:
        #     context['stock_sofala'] = 0
        # if context['stock_tete'] is None:
        #     context['stock_tete'] = 0
        # if context['stock_niassa'] is None:
        #     context['stock_niassa'] = 0
        return context
    
    def get_queryset(self):
        return Instrumento.objects.all()
    
   
    
class SectorListView(ListView):
    template_name = 'sector_list.html'
    context_object_name = 'sectores'
    paginate_by = 6
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
    paginate_by = 6
    context_object_name = 'instrumentos'
    model = Instrumento
    
      
    
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
    paginate_by = 6
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


def load_instrumentos(request):
    sector_id = request.GET.get('sector')
    instrumentos = Instrumento.objects.filter(sector_id=sector_id).order_by('nome')
    context = {'instrumentos': instrumentos}
    return render(request, 'instrumento_dropdown_list_options.html', context)

class ResumoListView(ListView):
    template_name = 'resumo_instrumentos.html'
    context_object_name = 'resumo_instrumentos'
    paginate_by = 6
    model = Resumo
    
    def get_queryset(self):
        qs = Resumo.objects.raw("select 1 AS id, p.nome AS provincia, s.nome AS sector, i.nome AS instrumento, i.stock,"\
                                  "i.quantidade_necessaria AS necessidade, i.ano, e.id AS entrada_id, e.data_entrada, e.quantidade AS quantidade_entrada, e.fornecedor,"\
                                  "r.id AS requisicao_id, r.data_requisicao, r.quantidade AS quantidade_requisitada, r.status_requisicao from core_instrumento i" \
                                  " inner join core_sector s on s.id=i.sector_id" \
                                  " inner join core_provincia p on i.provincia_id=p.id" \
                                  " left join core_entrada e on e.instrumento_id=i.id" \
                                  " left join core_requisicao r on r.instrumento_id=i.id"
                                   )
        return qs
    
    
       

class RequisicaoListView(ListView):
    template_name = 'requisicao_list.html'
    context_object_name = 'requisicoes'
    paginate_by = 6
    model = Requisicao
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('provincia')
        qs = qs.select_related('sector')
        qs = qs.select_related('instrumento')
        
        return qs
    
class RequisicaoCreateView(SuccessMessageMixin, CreateView):
    template_name = 'requisicao_create.html'
    form_class = RequisicaoForm
    success_url = '/'
    success_message = 'Requisicao adicionada com sucesso'
    
    def form_valid(self, form):
        requisicao = form.save(commit=False)
        requisicao.save()
        return redirect(self.success_url)
    
    
class RequisicaoUpdateView(UpdateView):
    template_name = 'requisicao_create.html'
    model = Requisicao
    success_url = '/requisicao/'
    fields = '__all__'
    pk_url_kwarg = 'pk'
    
    
    # def form_valid(self, form):
    #     requisicao = form.save(commit=False)
    #     requisicao.save()
    #     return redirect(self.success_url)
    
class RequisicaoDetailView(DetailView):
    model = Requisicao
    context_object_name = 'requisicao'
    template_name = 'requisicao_detail.html'
    pk_url_kwarg = 'pk'
    
class AprovarRequisicao(SuccessMessageMixin, CreateView):
    template_name = 'aprovacao_create.html'
    form_class = AprovacaoForm
    success_url = '/resumo'
    success_message = 'Requisicao adicionada com sucesso'
    
    def form_valid(self, form):
        aprovacao = form.save(commit=False)
        aprovacao.save()
        return redirect(self.success_url)
    
    def get_queryset(self):
        pass
    

def load_requisicoes(request):
    requisicao_id = request.GET.get('requisicao')
    requisicao = Requisicao.objects.filter(pk=requisicao_id).order_by('nome')
    context = {'requisicao': requisicao}
    return render(request, 'requisicao_dropdown_list_options.html', context)
       
    
    
