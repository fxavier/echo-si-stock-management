from os import path
from django.urls import path
from core.views import IndexView, TodosInstrumentosListView, InstrumentoCreateView, EntradasListView, EntradaCreateView, \
                       load_instrumentos, SectorListView, SectorCreateView, NecessidadeLisView, NecessidadeCreateView, \
                       load_sectores

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
    path('movimento/listar-sectores', load_sectores, name='listar_sectores'),
    path('necessidade/',NecessidadeLisView.as_view(), name='necessidade' ),
    path('necessidade/new', NecessidadeCreateView.as_view(), name='necessidade-new'),
]