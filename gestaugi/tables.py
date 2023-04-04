from django_tables2 import tables, TemplateColumn, Column
from .models import Socios, Lotes, Comparticipacoes, Assembleias, Presencas, Despesas, Anuidades, Pagamentos, TiposDespesas, Parametros

class SociosTable(tables.Table):
    TC1 = '<a class="btn btn-primary btn-xs" href="{% url "gestaugi:editpartner" record.socio_id %}">Editar</a>'
    Ações = TemplateColumn(TC1)

    class Meta:
         model = Socios
         attrs = {'class': 'table table-bordered table-condensed table-display'}
         #attrs = {'class': 'table table-xs table-hover'}
         template_name = "django_tables2/bootstrap4.html"
         fields = ['nome','nsocio', 'telemovel','email', 'lotes', 'compdivida','anuidivida',
                   'dt_admissao','estado']
         row_attrs = {
             "onClick": lambda record: "document.location.href='/viewpartner/{0}';".format(record.socio_id)
         }

class LotesTable(tables.Table):
    TC1 = '<a class="btn btn-primary btn-xs" href="{% url "gestaugi:editlot" record.lote_id %}">Editar</a>'
    Ações = TemplateColumn(TC1)

    class Meta:
         model = Lotes
         attrs = {'class': 'table table-bordered table-condensed table-display'}
         #attrs = {'class': 'table table-xs table-hover'}
         template_name = "django_tables2/bootstrap4.html"
         fields = ['socio.nome', 'nlote', 'area', 'local', 'dt_aquisicao', 'dt_venda','nfogos','frenteslote']
         row_attrs = {
             "onClick": lambda record: "document.location.href='/viewlot/{0}';".format(record.lote_id)
         }

class CompartTable(tables.Table):
    TC1 = '<a class="btn btn-primary btn-xs" href="{% url "gestaugi:editcoparticipation" record.compart_id %}">Editar</a>'
    Ações = TemplateColumn(TC1)

    class Meta:
         model = Comparticipacoes
         attrs = {'class': 'table table-bordered table-condensed table-display'}
         #attrs = {'class': 'table table-xs table-hover'}
         template_name = "django_tables2/bootstrap4.html"
         fields = ['socio.nome', 'lote.nlote', 'valor_calculado', 'descricao', 'tipo', 'dt_valor']
         row_attrs = {
             "onClick": lambda record: "document.location.href='/viewcoparticipation/{0}';".format(record.compart_id)
         }

class AssembleiasTable(tables.Table):
    TC1 = '<a class="btn btn-primary btn-xs" href="{% url "gestaugi:editassembly" record.assembleia_id %}">Editar</a>'
    Ações = TemplateColumn(TC1)

    class Meta:
         model = Assembleias
         attrs = {'class': 'table table-bordered table-condensed table-display'}
         #attrs = {'class': 'table table-xs table-hover'}
         template_name = "django_tables2/bootstrap4.html"
         fields = ['tipo','orgao','cpostal','localidade','dt_assembleia','convocados','presencas','rep_total','rep_assembl']
         row_attrs = {
             "onClick": lambda record: "document.location.href='/viewassembly/{0}';".format(record.assembleia_id)
         }


class PresencasTable(tables.Table):
    TC1 = '<a class="btn btn-primary btn-xs" href="{% url "gestaugi:editattendance" record.presenca_id %}">Editar</a>'
    Ações = TemplateColumn(TC1)

    class Meta:
        model = Presencas
        attrs = {'class': 'table table-bordered table-condensed table-display'}
        # attrs = {'class': 'table table-xs table-hover'}
        template_name = "django_tables2/bootstrap4.html"
        fields = ['socio.nome', 'orgao', 'dt_assembleia', 'representacao']
        row_attrs = {
            "onClick": lambda record: "document.location.href='/viewattendance/{0}';".format(record.presenca_id)
        }

class AnuidadesTable(tables.Table):
    TC1 = '<a class="btn btn-primary btn-xs" href="{% url "gestaugi:editannuity" record.anuidade_id %}">Editar</a>'
    Ações = TemplateColumn(TC1)

    class Meta:
         model = Anuidades
         attrs = {'class': 'table table-bordered table-condensed table-display'}
         #attrs = {'class': 'table table-xs table-hover'}
         template_name = "django_tables2/bootstrap4.html"
         fields = ['socio.nome','socio.nsocio','anuidade','ano']
         row_attrs = {
             "onClick": lambda record: "document.location.href='/viewannuity/{0}';".format(record.anuidade_id)
         }

class PagamentosTable(tables.Table):
    TC1 = '<a class="btn btn-primary btn-xs" href="{% url "gestaugi:editpayment" record.pagamento_id %}">Editar</a>'
    Ações = TemplateColumn(TC1)

    class Meta:
         model = Pagamentos
         attrs = {'class': 'table table-bordered table-condensed table-display'}
         #attrs = {'class': 'table table-xs table-hover'}
         template_name = "django_tables2/bootstrap4.html"
         fields = ['socio.nome','pagamento','tipo','descricao','dt_pagamento']
         row_attrs = {
             "onClick": lambda record: "document.location.href='/viewpayment/{0}';".format(record.pagamento_id)
         }

class TDespesasTable(tables.Table):
    TC1 = '<a class="btn btn-primary btn-xs" href="{% url "gestaugi:editexpensetype" record.tipo_id %}">Editar</a>'
    Ações = TemplateColumn(TC1)

    class Meta:
         model = TiposDespesas
         attrs = {'class': 'table table-bordered table-condensed table-display'}
         #attrs = {'class': 'table table-xs table-hover'}
         template_name = "django_tables2/bootstrap4.html"
         fields = ['tipo_id','descricao']
         row_attrs = {
             "onClick": lambda record: "document.location.href='/viewexpensetype/{0}';".format(record.tipo_id)
         }

class DespesasTable(tables.Table):
    TC1 = '<a class="btn btn-primary btn-xs" href="{% url "gestaugi:editexpense" record.despesa_id %}">Editar</a>'
    Ações = TemplateColumn(TC1)

    class Meta:
         model = Despesas
         attrs = {'class': 'table table-bordered table-condensed table-display'}
         #attrs = {'class': 'table table-xs table-hover'}
         template_name = "django_tables2/bootstrap4.html"
         fields = ['tipo.descricao','despesa','ano','dt_registo']
         row_attrs = {
             "onClick": lambda record: "document.location.href='/viewexpense/{0}';".format(record.despesa_id)
         }

class ParametrosTable(tables.Table):
    TC1 = '<a class="btn btn-primary btn-xs" href="{% url "gestaugi:editexpensetype" record.param_id %}">Editar</a>'
    Ações = TemplateColumn(TC1)

    class Meta:
         model = Parametros
         attrs = {'class': 'table table-bordered table-condensed table-display'}
         #attrs = {'class': 'table table-xs table-hover'}
         template_name = "django_tables2/bootstrap4.html"
         fields = ['vtotobra','tfrenlot','tfoglot','tarealot']
         row_attrs = {
             "onClick": lambda record: "document.location.href='/viewexpensetype/{0}';".format(record.param_id)
         }