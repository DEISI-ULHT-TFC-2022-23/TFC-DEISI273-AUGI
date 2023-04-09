from django.contrib import admin
from .models import Socios, Lotes, Comparticipacoes, Assembleias, Despesas, Anuidades, Pagamentos, Presencas, Parametros, CodPostais, AugiDashboard

# Register your models here.

admin.site.register(Socios)
admin.site.register(Lotes)
admin.site.register(Comparticipacoes)
admin.site.register(Assembleias)
admin.site.register(Despesas)
admin.site.register(Pagamentos)
admin.site.register(Parametros)
admin.site.register(Anuidades)
admin.site.register(CodPostais)
admin.site.register(Presencas)
admin.site.register(AugiDashboard)