import django_filters
from .models import Socios, Assembleias, Presencas, Anuidades, TiposDespesas

class SocioFilter(django_filters.FilterSet):
	nome = django_filters.CharFilter(lookup_expr='icontains',label="Nome")
	class Meta:
		model = Socios
		fields = {'nome'}

class LoteFilter(django_filters.FilterSet):
	CHOICES = Socios.objects.all().values_list('socio_id','nome').order_by('nome')
	result = django_filters.ChoiceFilter(empty_label='-------------------', label="Sócio",
										 choices=CHOICES, method="socio_id")
	def socio_id(self, queryset, name, value):
		return queryset.filter(socio_id=value)
	#nsocio_id = django_filters.AllValuesFilter(lookup_expr='exact',label="NºSocio")
	#class Meta:
	#	model = Lotes
    #		fields = {'nsocio_id'}

class CompartFilter(django_filters.FilterSet):
	CHOICES = Socios.objects.all().values_list('socio_id','nome').order_by('nome')
	result = django_filters.ChoiceFilter(empty_label='-------------------', label="Sócio",
										 choices=CHOICES, method="socio_id")
	def socio_id(self, queryset, name, value):
		return queryset.filter(socio_id=value)
	#nsocio_id = django_filters.AllValuesFilter(lookup_expr='exact',label="NºSocio")
	#class Meta:
    #   model = Comparticipacoes
	#	fields = {'nsocio_id'}

class AssembleiaFilter(django_filters.FilterSet):
	orgao = django_filters.AllValuesFilter(lookup_expr='exact',label="Orgão")
	dt_assembleia = django_filters.AllValuesFilter(lookup_expr='exact',label="Dt.Assemb.")
	class Meta:
		model = Assembleias
		fields = {'orgao','dt_assembleia'}

class PresencaFilter(django_filters.FilterSet):
	orgao = django_filters.AllValuesFilter(lookup_expr='exact',label="Orgão")
	dt_assembleia = django_filters.AllValuesFilter(lookup_expr='exact',label="Dt.Assemb.")
	class Meta:
		model = Presencas
		fields = {'orgao','dt_assembleia'}

class DespesasFilter(django_filters.FilterSet):
	CHOICES = TiposDespesas.objects.all().values_list('tipo_id','descricao').order_by('tipo_id')
	result = django_filters.ChoiceFilter(empty_label='---------------------------', label="Tipo",
										 choices=CHOICES, method="tdespesa")
	def tdespesa(self, queryset, name, value):
		return queryset.filter(tipo_id=value)
	#tipo = django_filters.AllValuesFilter(lookup_expr='exact',label="Tipo")
	# ano = django_filters.AllValuesFilter(lookup_expr='exact', label="Ano")
	# class Meta:
	# 	model = Despesas
	# 	fields = {'ano'}

class AnuidadesFilter(django_filters.FilterSet):
	CHOICES = Socios.objects.all().values_list('socio_id','nome').order_by('nome')
	result = django_filters.ChoiceFilter(empty_label='-------------------', label="Sócio",
										 choices=CHOICES, method="socio_id")
	def socio_id(self, queryset, name, value):
		return queryset.filter(socio_id=value)

	#nsocio = django_filters.AllValuesFilter(lookup_expr='exact',label="NºSocio")
	ano = django_filters.AllValuesFilter(lookup_expr='exact', label="Ano")
	class Meta:
		model = Anuidades
		fields = {'ano'}

class PagamentosFilter(django_filters.FilterSet):
	CHOICES = Socios.objects.all().values_list('socio_id','nome').order_by('nome')
	result = django_filters.ChoiceFilter(empty_label='-------------------', label="Sócio",
										 choices=CHOICES, method="socio_id")
	def socio_id(self, queryset, name, value):
		return queryset.filter(socio_id=value)

class TDespesasFilter(django_filters.FilterSet):
	descricao = django_filters.AllValuesFilter(lookup_expr='icontains',label="Descrição")
	class Meta:
		model = TiposDespesas
		fields = {'descricao'}