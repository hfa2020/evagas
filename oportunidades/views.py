from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Oportunidades, Candidaturas
from django.views.generic import DetailView, TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count
from django.db.models.functions import TruncMonth
from random import randint
from chartjs.views.lines import BaseLineChartView
from django.http import Http404

# Create your views here.


class OportunidadeDetailView(LoginRequiredMixin, DetailView):
    model = Oportunidades


class OportunidadeListView(LoginRequiredMixin, ListView):
    model = Oportunidades

    def get_queryset(self):
        if self.request.user.is_empresa:
            return Oportunidades.objects.filter(empresa=self.request.user)
        else:
            return Oportunidades.objects.all()


class OportunidadeUpdateView(LoginRequiredMixin, UpdateView):
    model = Oportunidades
    fields = '__all__'

    # template_name = 'home.html'
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.empresa != self.request.user:
            raise Http404("Você não tem permissão para editar este item.")
        return super().dispatch(request, *args, **kwargs)


class OportunidadeCreateView(LoginRequiredMixin, CreateView):
    model = Oportunidades
    fields = ['nome', 'requisitos', 'faixa_salario', 'escolaridade']
    success_url = reverse_lazy('ListaVagas')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_empresa:
            raise Http404("Você não tem permissão para editar este item.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.empresa = self.request.user

        return super().form_valid(form)


class OportunidadeDeleteView(LoginRequiredMixin, DeleteView):
    model = Oportunidades
    fields = '__all__'
    template_name = "oportunidades/oportunidades_form.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.empresa != self.request.user:
            raise Http404("Você não tem permissão para editar este item.")
        return super().dispatch(request, *args, **kwargs)

#Views Candidaturas


class CandidaturaListView(LoginRequiredMixin, ListView):
    model = Candidaturas

    def get_queryset(self):
        return Candidaturas.objects.filter(candidato=self.request.user)

class CandidaturaUpdateView(LoginRequiredMixin, UpdateView):
    model = Candidaturas
    fields = '__all__'

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.candidato != self.request.user:
            raise Http404("Você não tem permissão para editar este item.")
        return super().dispatch(request, *args, **kwargs)


class CandidaturaCreateView(LoginRequiredMixin, CreateView):
    model = Candidaturas
    fields = ['salario_pretendido']
    success_url = reverse_lazy('ListaVagas')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_empresa:
            raise Http404("Você não tem permissão para editar este item.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cand = Oportunidades.objects.get(pk=self.kwargs.get('pk'))
        context['vaga'] = cand
        return context

    def form_valid(self, form):
        form.instance.vaga = Oportunidades.objects.get(pk=self.kwargs['pk'])
        form.instance.candidato = self.request.user

        try:
            return super().form_valid(form)
        except IntegrityError:
            messages.add_message(self.request, messages.ERROR,
                                 'Você já se candidatou a esta vaga')
            return self.form_invalid(form)


class CandidaturaDeleteView(LoginRequiredMixin, DeleteView):
    model = Candidaturas
    fields = '__all__'

    template_name = "oportunidades/candidaturas_form.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.candidato != self.request.user:
            raise Http404("Você não tem permissão para editar este item.")
        return super().dispatch(request, *args, **kwargs)

class LineChartJSONView(LoginRequiredMixin, BaseLineChartView):
    def get_labels(self):
        """Return 12 labels for the x-axis."""
        return [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho",
            "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

    def get_providers(self):
        """Return names of datasets."""
        return ["Candidaturas", "Vagas"]

    def get_data(self):
        """Return 1 datasets to plot."""
        listaa = [0] * 12
        listab = [0] * 12
        lista = [listaa, listab]

        qs_candidaturas = Candidaturas.objects.filter(
            vaga__empresa=self.request.user).annotate(
                month=TruncMonth('data')).values('month').annotate(
                    total=Count('id'))
        qs_vagas = Oportunidades.objects.filter(
            empresa=self.request.user).annotate(
                month=TruncMonth('data')).values('month').annotate(
                    total=Count('id'))

        lista[0][(qs_candidaturas.get()["month"].month -
                  1)] = qs_candidaturas.get()["total"]
        lista[1][(qs_vagas.get()["month"].month - 1)] = qs_vagas.get()["total"]

        return lista

class EstatisticasView(LoginRequiredMixin, TemplateView):
    template_name='chart.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_empresa:
            raise Http404("Você não tem permissão para editar este item.")
        return super().dispatch(request, *args, **kwargs)


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()
