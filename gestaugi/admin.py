from django.contrib import admin
from .models import Socios, Lotes, Comparticipacoes, Assembleias, Despesas

# Register your models here.

admin.site.register(Socios)
admin.site.register(Lotes)
admin.site.register(Comparticipacoes)
admin.site.register(Assembleias)
admin.site.register(Despesas)

