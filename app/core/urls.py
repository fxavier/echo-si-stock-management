from os import path
from django.urls import path
from core.views import IndexView, TodosInstrumentosListView, InstrumentoCreateView, EntradasListView, EntradaCreateView, \
                       load_instrumentos, SectorListView, SectorCreateView, RequisicaoListView, RequisicaoCreateView, ResumoListView, \
                       AprovarRequisicao, load_requisicoes, RequisicaoUpdateView
                       

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('sector/', SectorListView.as_view(), name='sector'),
    path('sector/new', SectorCreateView.as_view(), name='sector-new'),
    path('instrumento/', TodosInstrumentosListView.as_view(), name='instrumento'),
    path('instrumento/new', InstrumentoCreateView.as_view(), name='instrumento-new'),
    path('movimento/', EntradasListView.as_view(), name='entrada'),
    path('movimento/new', EntradaCreateView.as_view(), name='entrada-new'),
    path('movimento/listar-instrumentos', load_instrumentos, name='listar_instrumentos'),
    path('requisicao/', RequisicaoListView.as_view(), name='requisicao'),
    path('requisicao/new', RequisicaoCreateView.as_view(), name='requisicao-new'),
    path('requisicao/edit/<int:pk>/', RequisicaoUpdateView.as_view(), name='requisicao-update'),
    path('resumo/', ResumoListView.as_view(), name='resumo'),
    path('aprovacao/<int:requisicao_id>/requisicao', AprovarRequisicao.as_view(), name='aprovacao'),
    path('aprovacao/requisicao', load_requisicoes, name='aprovacao-requisicao'),
  
]