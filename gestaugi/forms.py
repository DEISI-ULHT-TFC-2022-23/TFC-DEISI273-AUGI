from django import forms
from django.forms import ModelForm
from .models import CodPostais, Socios, Lotes, Comparticipacoes, Assembleias, Presencas, Despesas, Anuidades, Pagamentos, TiposDespesas

STATUS_CHOICES = [
    ('Ativo', 'Ativo'),
    ('Inativo', 'Inativo'),
    ('Anulado', 'Anulado'),
    ('Suspenso', 'Suspenso'),
    ]

ASSEMBLY_ORGAN_CHOICES = [
    ('AUGI', 'AUGI'),
    ('Associação', 'Associação'),
    ]

ASSEMBLY_TYPE_CHOICES = [
    ('Ordinária', 'Ordinária'),
    ('Especial', 'Especial'),
    ]

PAYMENT_TYPE_CHOICES = [
    ('Anuidade', 'Anuidade'),
    ('Comparticipação', 'Comparticipação'),
]

# cria o form baseado no modelo
#Formulario para inserção e edição
class SocioForm(ModelForm):
    class Meta:
        model = Socios
        fields = '__all__'
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'nsocio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nsocio', 'size': '10'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'nome','size' : '30'}),
            'morada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'morada','size' : '30'}),
            'localidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'localidade', 'size': '30'}),
            'cpostal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1000-001', 'size': '8'}),
            'cpostlocal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'localidade do cod.postal', 'size': '30'}),
            'telemovel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '912123123'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@dominio.com', 'size': '40'}),
            'lotes': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'lotes', 'size': '20'}),
            'representacao' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'representação', 'size': '10'}),
            'compdivida' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'comp.divida', 'size': '10'}),
            'anuididiva' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'anui.divida', 'size': '10'}),
            'dt_admissao': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa','type': 'date'}),
            'estado': forms.Select(choices=STATUS_CHOICES),
         }

    # texto a exibir junto à janela de inserção
        labels = {
            'nsocio': 'NºSocio',
            'nome': 'Nome',
            'morada': 'Morada',
            'localidade': 'Localidade',
            'costal': 'CodPostal',
            'cpostlocal': 'Local.Cod.Postal',
            'telemovel': 'Telemovel',
            'email': 'Email',
            'lotes': 'Lotes',
            'representacao' : 'Representação',
            'compdivida': 'Comp.Devidas',
            'anuidivida': 'Anuid.Devidas',
            'dt_admissao': 'Dt.Admissão',
            'estado': 'Estado',
        }

        error_messages = {
            'nome': {
                '': ("Tem de preencher este campo."),
            },
        }

    # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'Introduza dados...',
        }

# Formulário só para consulta
class SocioViewForm(ModelForm):
    class Meta:
        model = Socios
        fields = '__all__'
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'nsocio': forms.NumberInput(attrs={'class': 'form-control', 'size': '10','readonly': 'True'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'size' : '30','readonly': 'True'}),
            'morada': forms.TextInput(attrs={'class': 'form-control', 'size' : '30','readonly': 'True'}),
            'localidade': forms.TextInput(attrs={'class': 'form-control', 'size': '30', 'readonly': 'True'}),
            'cpostal': forms.TextInput(attrs={'class': 'form-control', 'size': '8','readonly': 'True'}),
            'cpostlocal': forms.TextInput(attrs={'class': 'form-control', 'size': '30', 'readonly': 'True'}),
            'telemovel': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'size': '40','readonly': 'True'}),
            'lotes': forms.TextInput(attrs={'class': 'form-control',  'size': '10','readonly': 'True'}),
            'representacao': forms.NumberInput(attrs={'class': 'form-control', 'size': '10', 'readonly': 'True'}),
            'compdivida': forms.NumberInput(attrs={'class': 'form-control', 'size': '10','readonly': 'True'}),
            'anuididiva': forms.NumberInput(attrs={'class': 'form-control', 'size': '10','readonly': 'True'}),
            'dt_admissao': forms.DateInput(format=('%d/%m/%Y'),attrs={'class': 'form-control', 'readonly': 'True'}),
            'estado' :  forms.TextInput(attrs={'class': 'form-control', 'size': '10','readonly': 'True'}),
        }

# cria o form baseado no modelo
#Formulario para inserção e edição
class LoteForm(ModelForm):
    class Meta:
        model = Lotes
        fields = ('nlote','area','local','dt_aquisicao','dt_venda','nfogos','frenteslote',)
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'nlote': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'nlote', 'size': '20'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'area','size' : '30', 'min' : '0'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'local','size' : '30'}),
            'dt_aquisicao': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa', 'type' : 'date'}),
            'dt_venda': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control','placeholder': 'dd/mm/aaaa', 'type' : 'date'}),
            'nfogos': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '999', 'size':'10', 'min' : '0'}),
            'frenteslote': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '999', 'size': '10', 'min' : '0'}),
        }

    # texto a exibir junto à janela de inserção
        labels = {
            'nlote' : 'NºLote',
            'area': 'Area',
            'local': 'Local',
            'dt_aquisicao': 'Dt.Aquisicao',
            'dt_venda': 'Dt.Venda',
            'nfogos': 'NºFogos',
            'frenteslote': 'FrentesLote'
        }

        error_messages = {
            'area': {
                '': ("Tem de preencher este campo."),
            },
        }

    # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'Introduza dados...',
        }

# Formulário só para consulta
class LoteViewForm(ModelForm):
    class Meta:
        model = Lotes
        fields = ('nlote','area','local','dt_aquisicao','dt_venda','nfogos','frenteslote',)
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'nlote': forms.NumberInput(attrs={'class': 'form-control', 'size': '10', 'readonly': 'True'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'size' : '30', 'readonly': 'True'}),
            'local': forms.TextInput(attrs={'class': 'form-control', 'size' : '30','readonly': 'True' }),
            'dt_aquisicao': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'type' : 'date', 'readonly': 'True'}),
            'dt_venda': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'type' : 'date', 'readonly': 'True'}),
            'nfogos': forms.NumberInput(attrs={'class': 'form-control', 'size':'10', 'readonly': 'True'}),
            'frenteslote': forms.NumberInput(attrs={'class': 'form-control', 'size': '10','readonly': 'True'}),
        }

# cria o form baseado no modelo
#Formulario para inserção e edição
class CompartForm(ModelForm):
    class Meta:
        model = Comparticipacoes
        fields = ('valor_calculado','descricao','tipo','dt_valor','dt_registo','estado','dt_estado')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'valor_calculado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'valor', 'size': '10'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'descrição','size' : '50'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'tipo','size' : '30'}),
            'dt_valor': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa', 'type' : 'date'}),
            'dt_registo': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'type' : 'date','readonly': 'True'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'estado','size' : '30'}),
            'dt_estado': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'type' : 'date', 'readonly': 'True'}),
        }

    # texto a exibir junto à janela de inserção
        labels = {
            'valor_calculado' : 'Valor',
            'descricao': 'Descrição',
            'tipo': 'Tipo',
            'dt_valor': 'Dt.Valor',
            'dt_registo': 'Dt.Registo',
            'estado': 'Estado',
            'dt_estado': 'Dt.Estado',
        }

        error_messages = {
            'valor_calculado': {
                '': ("Tem de preencher este campo."),
            },
        }

    # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'Introduza dados...',
        }

#Formulario para consulta
class CompartViewForm(ModelForm):
    class Meta:
        model = Comparticipacoes
        fields = ('valor_calculado','descricao','tipo','dt_valor','dt_registo','estado','dt_estado')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'valor_calculado': forms.NumberInput(attrs={'class': 'form-control', 'size': '10', 'readonly': 'True'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control','size' : '50', 'readonly': 'True'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'size' : '30', 'readonly': 'True'}),
            'dt_valor': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'type' : 'date', 'readonly': 'True'}),
            'dt_registo': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'type' : 'date','readonly': 'True'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'size' : '30' , 'readonly': 'True'}),
            'dt_estado': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'type' : 'date', 'readonly': 'True'}),
        }


# cria o form baseado no modelo
#Formulario para inserção e edição
class AssembleiaForm(ModelForm):
    class Meta:
        model = Assembleias
        fields = '__all__'
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'tipo': forms.Select(choices=ASSEMBLY_TYPE_CHOICES),
            'orgao': forms.Select(choices=ASSEMBLY_ORGAN_CHOICES),
            'cpostal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1000-000', 'size': '8'}),
            'localidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'localidade', 'size': '70'}),
            'dt_assembleia': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa','type': 'date'}),
            'convocados': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'convocados', 'size': '10'}),
            'presencas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'presenças', 'size': '10'}),
            'rep_total': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'rep.total', 'size': '10'}),
            'rep_socios': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'rep.socios', 'size': '10'}),
            'rep_assembl': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'rep.assembleia', 'size': '10'}),
         }

    # texto a exibir junto à janela de inserção
        labels = {
            'tipo': 'Tipo',
            'orgao': 'Orgão',
            'cpostal': 'Cod.Postal',
            'localidade': 'Localidade',
            'dt_assembleia': 'Dt.Assembleia',
            'convocados': 'Convocados',
            'presencas': 'Presenças',
            'rep_total': 'Rep.Total',
            'rep_socios': 'Rep.Socios',
            'rep_assembl': 'Rep.Assembleia',

        }

        error_messages = {
            'nome': {
                '': ("Tem de preencher este campo."),
            },
        }

    # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'Introduza dados...',
        }

#Formulario para consulta
class AssembleiaViewForm(ModelForm):
    class Meta:
        model = Assembleias
        fields = '__all__'
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'size': '8', 'readonly': 'True'}),
            'orgao': forms.TextInput(attrs={'class': 'form-control', 'size': '8', 'readonly': 'True'}),
            'cpostal': forms.TextInput(attrs={'class': 'form-control', 'size': '8', 'readonly': 'True'}),
            'localidade': forms.TextInput(attrs={'class': 'form-control', 'size': '70','readonly': 'True'}),
            'dt_assembleia': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'type': 'date','readonly': 'True'}),
            'convocados': forms.NumberInput(attrs={'class': 'form-control', 'size': '10','readonly': 'True'}),
            'presencas': forms.NumberInput(attrs={'class': 'form-control', 'size': '10','readonly': 'True'}),
            'rep_total': forms.NumberInput(attrs={'class': 'form-control',  'size': '10', 'readonly': 'True'}),
            'rep_assembl': forms.NumberInput(attrs={'class': 'form-control', 'size': '10', 'readonly': 'True'}),
         }

# cria o form baseado no modelo
#Formulario para inserção e edição
class PresencaForm(ModelForm):
    class Meta:
        model = Presencas
        fields = ('orgao','representacao')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'orgao': forms.Select(choices=ASSEMBLY_ORGAN_CHOICES),
            #'dt_assembleia': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa','type': 'date'}),
            'representacao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'representação', 'size': '10'}),
         }

    # texto a exibir junto à janela de inserção
        labels = {
            'orgao': 'Orgão',
            'dt_assembleia': 'Dt.Assembleia',
            'representacao': 'Representação',
         }

        error_messages = {
            'nome': {
                '': ("Tem de preencher este campo."),
            },
        }

    # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'Introduza dados...',
        }

#Formulario para consulta
class PresencaViewForm(ModelForm):
    class Meta:
        model = Presencas
        fields = ('orgao','representacao')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'orgao': forms.TextInput(attrs={'class': 'form-control', 'size': '8', 'readonly': 'True'}),
            #'dt_assembleia': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa','type': 'date'}),
            'representacao': forms.NumberInput(attrs={'class': 'form-control', 'size': '10','readonly': 'True'}),
         }


# cria o form baseado no modelo
#Formulario para inserção e edição
class DespesasForm(ModelForm):
    class Meta:
        model = Despesas
        fields = ('despesa','ano','descricao','dt_registo')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'despesa': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'despesa', 'size': '10'}),
            'ano' : forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ano', 'size': '6'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'descrição','size' : '70'}),
            'dt_registo': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date', 'readonly': 'True'}),
        }

    # texto a exibir junto à janela de inserção
        labels = {
            'tipo' : 'Tipo',
            'despesa': 'Despesa',
            'ano' : 'Ano',
            'descricao': 'Descrição',
        }

    # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'Introduza dados...',
        }

#Formulario para consulta
class DespesasViewForm(ModelForm):
    class Meta:
        model = Despesas
        fields = ('despesa','ano','descricao','dt_registo')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'despesa': forms.NumberInput(attrs={'class': 'form-control',  'size': '10', 'readonly': 'True'}),
            'ano' : forms.NumberInput(attrs={'class': 'form-control',  'size': '6', 'readonly': 'True'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control','size' : '70', 'readonly': 'True'}),
            'dt_registo': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date', 'readonly': 'True'}),
        }

# cria o form baseado no modelo
#Formulario para inserção e edição
class AnuidadesForm(ModelForm):
    class Meta:
        model = Anuidades
        fields = ('anuidade','ano','dt_pagamento')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'anuidade': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'anuidade', 'size': '10'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ano', 'size': '6'}),
            'dt_pagamento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa', 'type': 'date'}),
        }

    # texto a exibir junto à janela de inserção
        labels = {
            'anuidade': 'Anuidade',
            'ano' : 'Ano Referência',
            'dt_pagamento': 'Dt.Pagamento',
        }

    # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'Introduza dados...',
        }

#Formulario para consulta
class AnuidadesViewForm(ModelForm):
    class Meta:
        model = Anuidades
        fields = ('anuidade','ano','dt_pagamento')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'anuidade': forms.NumberInput(attrs={'class': 'form-control',  'size': '10', 'readonly': 'True'}),
            'ano': forms.NumberInput(attrs={'class': 'form-control', 'size': '6', 'readonly': 'True'}),
            'dt_pagamento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date', 'readonly': 'True'}),
        }

# cria o form baseado no modelo
#Formulario para inserção e edição
class PagamentosForm(ModelForm):
    class Meta:
        model = Pagamentos
        fields = ('pagamento','tipo','descricao','dt_pagamento')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'pagamento': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'pagamento', 'size': '10'}),
            'tipo': forms.Select(choices=PAYMENT_TYPE_CHOICES),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'descrição','size' : '70'}),
            'dt_pagamento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'placeholder': 'dd/mm/aaaa', 'type': 'date'}),
        }

    # texto a exibir junto à janela de inserção
        labels = {
            'pagamento': 'Pagamento',
            'tipo' : 'Tipo',
            'descricao' : 'Descrição',
            'dt_pagamento': 'Dt.Pagamento',
        }

    # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'Introduza dados...',
        }

# cria o form baseado no modelo
#Formulario para consulta
class PagamentosViewForm(ModelForm):
    class Meta:
        model = Pagamentos
        fields = ('pagamento','tipo','descricao','dt_pagamento')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'pagamento': forms.NumberInput(attrs={'class': 'form-control', 'size': '10', 'readonly': 'True'}),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'size': '10','readonly': 'True'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'size' : '70', 'readonly': 'True'}),
            'dt_pagamento': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type': 'date', 'readonly': 'True'}),
        }

# cria o form baseado no modelo
#Formulario para inserção e edição
class TiposDespesasForm(ModelForm):
    class Meta:
        model = TiposDespesas
        fields = ('tipo_id','descricao')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'id_tipo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '', 'size': '10'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'descrição','size' : '70'}),
        }

    # texto a exibir junto à janela de inserção
        labels = {
            'id_tipo' : 'Tipo',
            'descricao': 'Descrição',

        }

    # texto auxiliar a um determinado campo do formulário
        help_texts = {
            'Introduza dados...',
        }

#Formulario para consulta
class TiposDespesasViewForm(ModelForm):
    class Meta:
        model = TiposDespesas
        fields = ('tipo_id','descricao')
    # inserção de classes CSS para formatação de cada campo do formulário
        widgets = {
            'id_tipo': forms.NumberInput(attrs={'class': 'form-control',  'size': '10', 'readonly': 'True'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'size' : '70', 'readonly': 'True'}),
        }

class ImportForm(forms.Form):
    xls_name = forms.CharField(max_length=200)
