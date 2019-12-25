from django.urls import path
from django.views.generic import TemplateView
from .views import OportunidadeDetailView, OportunidadeListView, OportunidadeCreateView, OportunidadeUpdateView, OportunidadeDeleteView
from .views import CandidaturaListView, CandidaturaCreateView, CandidaturaUpdateView, CandidaturaDeleteView
from .views import LineChartJSONView, line_chart_json, EstatisticasView

urlpatterns = [
    #Views Vagas
    path('', OportunidadeListView.as_view(), name="ListaVagas"),
    path('criar/', OportunidadeCreateView.as_view(), name="Createvaga"),
    path('editar/<int:pk>', OportunidadeUpdateView.as_view(), name="UpdateVaga"),
    path('deletar/<int:pk>', OportunidadeDeleteView.as_view(), name="DeletaVaga"),
    path('info/<int:pk>', OportunidadeDetailView.as_view(), name="VagaInfo"),
    #Views Candidatura
    path('candidaturas', CandidaturaListView.as_view(), name="ListaCands"),
    path('candidatar/<int:pk>', CandidaturaCreateView.as_view(), name="novaCandidatura"),
    path('cancelar/<int:pk>', CandidaturaDeleteView.as_view(), name="Cancelar"),
    #ViewChart
    path('estatisticas/', EstatisticasView.as_view(), name="stats"),
    path('charts/', line_chart_json, name='charts')
]
