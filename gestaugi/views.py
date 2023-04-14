from django.shortcuts import render
from .models import Socios, Lotes, Comparticipacoes, Assembleias, Presencas, Despesas, Anuidades, Pagamentos, TiposDespesas, Parametros, AugiDashboard
from django.db.models import Sum
from .forms import SocioForm, SocioViewForm, LoteForm, LoteViewForm, CompartForm, CompartViewForm, AssembleiaForm
from .forms import AssembleiaViewForm, PresencaForm, PresencaViewForm, DespesasForm, DespesasViewForm, AnuidadesForm
from .forms import AnuidadesViewForm, PagamentosForm, PagamentosViewForm, TiposDespesasForm, TiposDespesasViewForm
from .tables import SociosTable, LotesTable, CompartTable, AssembleiasTable, PresencasTable, PagamentosTable, DespesasTable
from .tables import AnuidadesTable, TDespesasTable, ParametrosTable
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .filters import SocioFilter, LoteFilter, CompartFilter, AssembleiaFilter, PresencaFilter, DespesasFilter, AnuidadesFilter
from .filters import PagamentosFilter, TDespesasFilter
from .utils import save2pdf
from .querys import sql_debts, sql_expenses, sql_totexpenses, sql_areas, sql_payments
from django.db.models.deletion import ProtectedError, IntegrityError
from decimal import Decimal
import datetime
import csv

# Create your views here.
def home_page_view(request):
	return render(request, 'gestaugi/home.html')

def partners_page_view(request):
	socios = Socios.objects.all().order_by("nsocio")
	filtro = SocioFilter(request.GET,socios)
	table = SociosTable(filtro.qs)
	table.paginate(page=request.GET.get("page", 1), per_page=10)
	return render(request, 'gestaugi/partners.html',
				  context={"model":socios, "table":table, "filter": filtro})

def newpartner(request):
	form = SocioForm(request.POST or None)
	if form.is_valid():
		# A singularidade do nº de sócio é garantida pelas regras de integridade implementadas no modelo
		form.save()
		return HttpResponseRedirect(reverse('gestaugi:partners'))
	else:
		print(form.errors)
	return render(request, 'gestaugi/newpartner.html', {
	  'form': form
	})

def viewpartner(request,socio_id):
	socio = Socios.objects.get(pk=socio_id)
	form = SocioViewForm(request.POST or None, instance=socio)
	return render(request, 'gestaugi/viewpartner.html', {
	  'form': form, 'socio' : socio
	})

def editpartner(request,socio_id):
	socio = Socios.objects.get(pk=socio_id)
	form = SocioForm(request.POST or None, instance=socio)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaugi:partners'))
	else:
		print(form.errors)
	return render(request, 'gestaugi/editpartner.html', {
	  'form': form, 'socio' : socio
	})

def deletepartner(request,socio_id):
	instance = Socios.objects.get(socio_id=socio_id)
	try:
		instance.delete()
		return HttpResponseRedirect(reverse('gestaugi:partners'))
	except ProtectedError:
		messages.add_message(request, messages.INFO, 'Sócio com Lotes e Comparticipações. Não é possivel suprimir!')
		#return HttpResponseRedirect(reverse('gestaugi:dispmessage'))
		return render(request,'gestaugi/messages.html',{'url':'/partners'})

def lots_page_view(request):
	lotes = Lotes.objects.all().order_by("nlote")
	filtro = LoteFilter(request.GET,lotes)
	table = LotesTable(filtro.qs)
	table.paginate(page=request.GET.get("page", 1), per_page=10)
	return render(request, 'gestaugi/lots.html',
				  context={"model":lotes, "table":table, "filter": filtro})

def newlot(request):
	#Lista de socios para escolha / associar ao lote
	socios = Socios.objects.all().values('socio_id','nsocio','nome').order_by('nome')
	form = LoteForm(request.POST or None)
	if form.is_valid():
		#Verificar se o lote já se encontra atribuido a outro socio e sem data de venda
		nlote = request.POST.get('nlote',None)
		existslote = Lotes.objects.select_related('socio').filter(nlote=nlote,dt_venda__isnull=True)
		dtvenda = False
		# Podem existir varios registos do mesmo lote já vendidos
		for lote in existslote:
			if lote.dt_venda != None:
				dtvenda = True
		print(existslote.count())
		print(dtvenda)
		if existslote.count() > 0 and not dtvenda:
			messages.add_message(request, messages.INFO, 'Lote ' + nlote + ' já atribuido ao sócio ' + existslote[0].socio.nome + ' !')
			# return HttpResponseRedirect(reverse('gestaugi:dispmessage'))
			return render(request, 'gestaugi/messages.html', {'url': '/lots'})
		else:
			instance = form.save(commit=False)
			instance.socio_id = request.POST.get('socio', None)
			if (instance.socio_id == 'Escolha sócio...'):
				messages.add_message(request, messages.INFO, 'Tem de escolher um sócio!')
				return render(request, 'gestaugi/messages.html', {'url': '/newlot'})
			else:
				instance.save()
				return HttpResponseRedirect(reverse('gestaugi:lots'))
	else:
		print(form.errors)
		#form = LoteForm()
	return render(request, 'gestaugi/newlot.html', {
	  'form': form, 'socios' : socios
	})

def viewlot(request,lote_id):
	lote = Lotes.objects.get(pk=lote_id)
	# Id do Socio dono do lote
	socio_id = Lotes.objects.get(pk=lote_id).socio_id
	# Vai buscar o nome do Socio a tabela de sócios, vai ficar selecionado no dropdown
	socios = Socios.objects.all().values('nsocio', 'nome').filter(pk=socio_id)
	form = LoteViewForm(request.POST or None, instance=lote)
	return render(request, 'gestaugi/viewlot.html', {
	   'form': form, 'socios' : socios, 'lote' : lote,
	})

def editlot(request,lote_id):
	lote = Lotes.objects.get(pk=lote_id)
	# Id do Socio dono do lote
	socio_id = Lotes.objects.get(pk=lote_id).socio_id
	# Vai buscar o nome do Socio a tabela de sócios, vai ficar selecionado no dropdown
	socios = Socios.objects.all().values('nsocio', 'nome').filter(pk=socio_id)
	form = LoteForm(request.POST or None, instance=lote)
	if form.is_valid():
		#Verificar se o lote já se encontra atribuido a outro socio e sem data de venda
		nlote = request.POST.get('nlote',None)
		existslote = Lotes.objects.select_related('socio').filter(nlote=nlote)
		dtvenda = False
		# Podem existir varios registos do mesmo lote já vendidos
		for lote in existslote:
			if lote.dt_venda != None:
				dtvenda = True
		if existslote.count() > 0 and not dtvenda:
			messages.add_message(request, messages.INFO, 'Lote ' + nlote + ' já atribuido ao sócio ' + existslote[0].socio.nome + ' !')
			# return HttpResponseRedirect(reverse('gestaugi:dispmessage'))
			return render(request, 'gestaugi/messages.html', {'url': '/lots'})
		else:
			form.save()
			return HttpResponseRedirect(reverse('gestaugi:lots'))
	else:
		print(form.errors)
	return render(request, 'gestaugi/editlot.html', {
	  'form': form, 'socios' : socios, 'lote' : lote,
	})

def deletelot(request,lote_id):
	instance = Lotes.objects.get(lote_id=lote_id)
	instance.delete()
	return HttpResponseRedirect(reverse('gestaugi:lots'))

def coparticipation_page_view(request):
	compart = Comparticipacoes.objects.all().order_by("compart_id")
	filtro = CompartFilter(request.GET,compart)
	table = CompartTable(filtro.qs)
	table.paginate(page=request.GET.get("page", 1), per_page=10)
	return render(request, 'gestaugi/coparticipation.html',
				  context={"model":compart, "table":table, "filter": filtro})

def newcoparticipation(request):
	# Lista de socios para escolha
	socios = Socios.objects.all().values('socio_id','nsocio','nome').order_by('nome')
	#Parametros - Valores totais para calculo da comparticipação
	param = Parametros.objects.all().filter(pk=1).values('vtotobra','tfrenlot','tfoglot','tarealot')
	if param.count() > 0:
		vtotobra = param[0]['vtotobra']
		tfrenlot = param[0]['tfrenlot']
		tfoglot = param[0]['tfoglot']
		tarealot = param[0]['tarealot']
	else:
		vtotobra = 0
		tfrenlot = 0
		tfoglot = 0
		tarealot = 0
	#Lista de lotes para escolha, inclui socios
	lotes = Lotes.objects.all()
	form = CompartForm(request.POST or None,initial={"dt_registo": datetime.date.today(),
													 "dt_estado": datetime.date.today(),
													 "estado": "Registado"})
	if form.is_valid():
		instance = form.save(commit=False)
		socio_id = request.POST.get('socio', None)
		lote_id = request.POST.get('lote', None)
		if (socio_id == 'Escolha sócio...'):
			messages.add_message(request, messages.INFO, 'Tem de escolher um sócio!')
			return render(request, 'gestaugi/messages.html', {'url': '/newcoparticipation'})
		elif (lote_id == 'Escolha lote...'):
			messages.add_message(request, messages.INFO, 'Tem de escolher um lote!')
			return render(request, 'gestaugi/messages.html', {'url': '/newcoparticipation'})
		# Vai buscar o valor de comparticipação que o sócio tem em divida
		compdivida = Socios.objects.filter(pk=socio_id).values('compdivida')[0]['compdivida']
        # Adiciona o novo valor de comparticipação
		compdivida = compdivida + Decimal(request.POST.get('valor_calculado',0))
		# Chaves estrangeiras
		instance.socio_id = socio_id
		instance.lote_id = lote_id
		# Regista a nova comparticipação
		instance.save()
		# Regista na tabela de Sócios o novo valor de comparticipação em divida
		Socios.objects.filter(pk=socio_id).update(compdivida=compdivida)
		return HttpResponseRedirect(reverse('gestaugi:coparticipation'))
	else :
		print(form.errors)
		#form = LoteForm()
	return render(request, 'gestaugi/newcoparticipation.html', {
	  'form': form, 'socios' : socios, 'lotes' : lotes, 'vtotobra' : vtotobra, 'tfrenlot' : tfrenlot,
		'tfoglot' : tfoglot, 'tarealot' : tarealot
	})

def load_lots(request):
    socio_id = request.GET.get('socio')
    lotes = Lotes.objects.filter(socio_id=socio_id).order_by('nlote')
    return render(request, 'gestaugi/load_lots.html', {'lotes': lotes})

def editcoparticipation(request,compart_id):
	compart = Comparticipacoes.objects.get(pk=compart_id)
	# Se comparticiação é alterada o valor anterior precisa de ser anulado no registo do sócio
	valor_anterior = compart.valor_calculado
	#Parametros - Valores totais para calculo da comparticipação
	param = Parametros.objects.all().filter(pk=1).values('vtotobra','tfrenlot','tfoglot','tarealot')
	vtotobra = param[0]['vtotobra']
	tfrenlot = param[0]['tfrenlot']
	tfoglot = param[0]['tfoglot']
	tarealot = param[0]['tarealot']
	#Lote, inclui socio
	lote = Lotes.objects.select_related('socio').all().filter(pk=compart.lote_id)
	form = CompartForm(request.POST or None,instance=compart)
	if form.is_valid():
		instance = form.save(commit=False)
		socio_id = request.POST.get('socio', None)
		lote_id = request.POST.get('lote', None)
		# Vai buscar o valor de comparticipação que o sócio tem em divida
		compdivida = Socios.objects.filter(pk=socio_id).values('compdivida')[0]['compdivida']
		# Retira valor anterior
		compdivida = compdivida - valor_anterior
		# Adiciona o novo valor de comparticipação
		compdivida = compdivida + Decimal(request.POST.get('valor_calculado', 0))
		# Chaves estrangeiras
		instance.socio_id = socio_id
		instance.lote_id = lote_id
		# Grava os dados do form
		instance.save()
		# Regista na tabela de Sócios o novo valor de comparticipação em divida
		Socios.objects.filter(pk=socio_id).update(compdivida=compdivida)
		return HttpResponseRedirect(reverse('gestaugi:coparticipation'))
	else :
		print(form.errors)
		#form = CompartForm()
	return render(request, 'gestaugi/editcoparticipation.html', {
	  'form': form, 'lote' : lote, 'compart' : compart, 'vtotobra' : vtotobra, 'tfrenlot' : tfrenlot,
		'tfoglot' : tfoglot, 'tarealot' : tarealot
	})

def viewcoparticipation(request,compart_id):
	compart = Comparticipacoes.objects.get(pk=compart_id)
	#Lote, inclui socio
	lote = Lotes.objects.select_related('socio').all().filter(pk=compart.lote_id)
	form = CompartViewForm(request.POST or None,instance=compart)
	return render(request, 'gestaugi/viewcoparticipation.html', {
	  'form': form, 'lote' : lote, 'compart' : compart
	})

def deletecoparticipation(request,compart_id):
	instance = Comparticipacoes.objects.get(compart_id=compart_id)
	# Se comparticiação é suprimida o valor precisa de ser anulado no registo do sócio
	valor_anterior = instance.valor_calculado
	socio_id = instance.socio_id
	# Vai buscar o valor em divida no registo so sócio
	compdivida = Socios.objects.filter(pk=socio_id).values('compdivida')[0]['compdivida']
	# E retira o valor a suprimir
	compdivida = compdivida - valor_anterior
	instance.delete()
	# Regista na tabela de Sócios o valor de comparticipação em divida atualizado
	Socios.objects.filter(pk=socio_id).update(compdivida=compdivida)
	return HttpResponseRedirect(reverse('gestaugi:coparticipation'))

def assembly_page_view(request):
	assembleia = Assembleias.objects.all().order_by("assembleia_id")
	filtro = AssembleiaFilter(request.GET,assembleia)
	table = AssembleiasTable(filtro.qs)
	table.paginate(page=request.GET.get("page", 1), per_page=10)
	return render(request, 'gestaugi/assembly.html',
				  context={"model": assembleia, "table":table, "filter": filtro})

def newassembly(request):
	#Representação total - total das areas adquiridas
	rept_total = Lotes.objects.all().aggregate(Sum('area'))
	form = AssembleiaForm(request.POST or None, initial={'rep_total': rept_total['area__sum']})
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaugi:assembly'))
	else:
		print(form.errors)
	return render(request, 'gestaugi/newassembly.html', {
	  'form': form
	})

def editassembly(request,assembleia_id):
	assembleia = Assembleias.objects.get(pk=assembleia_id)
	form = AssembleiaForm(request.POST or None, instance=assembleia)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaugi:assembly'))
	else:
		print(form.errors)
	return render(request, 'gestaugi/editassembly.html', {
	  'form': form, 'assembleia' : assembleia
	})

def viewassembly(request,assembleia_id):
	assembleia = Assembleias.objects.get(pk=assembleia_id)
	form = AssembleiaViewForm(request.POST or None, instance=assembleia)
	return render(request, 'gestaugi/viewassembly.html', {
	  'form': form, 'assembleia' : assembleia
	})

def deleteassembly(request,assembleia_id):
	instance = Assembleias.objects.get(assembleia_id=assembleia_id)
	presencas = Assembleias.objects.filter(assembleia_id=assembleia_id).values('presencas')[0]['presencas']
	if presencas == 0:
		instance.delete()
		return HttpResponseRedirect(reverse('gestaugi:assembly'))
	else:
		messages.add_message(request, messages.INFO, 'Assembleia com presenças registas ! Não é possivel suprimir !')
		# return HttpResponseRedirect(reverse('gestaugi:dispmessage'))
		return render(request, 'gestaugi/messages.html', {'url': '/assembly'})

def attendance_page_view(request):
	presenca = Presencas.objects.all().order_by("socio")
	filtro = PresencaFilter(request.GET,presenca)
	table = PresencasTable(filtro.qs)
	table.paginate(page=request.GET.get("page", 1), per_page=10)
	return render(request, 'gestaugi/attendance.html',
				  context={"model": presenca, "table":table, "filter": filtro})

def newattendance(request):
	# Lista de socios para escolha
	#socios = Socios.objects.all().values('socio_id','nsocio','nome').order_by('nome')
	socios = Socios.objects.raw(sql_areas) # Raw sql inclui area total do sócio
	datas = Assembleias.objects.all().values('assembleia_id','dt_assembleia').order_by('dt_assembleia')
	form = PresencaForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		# Chave estrangeira
		socio_id = request.POST.get('socio', None)
		data = request.POST.get('data', None)
		if (socio_id == 'Escolha sócio...'):
			messages.add_message(request, messages.INFO,'Tem de escolher um sócio!')
			return render(request, 'gestaugi/messages.html', {'url': '/newattendance'})
		if (data == 'Escolha data...'):
			messages.add_message(request, messages.INFO,'Tem de escolher uma data!')
			return render(request, 'gestaugi/messages.html', {'url': '/newattendance'})
		orgao = request.POST.get('orgao',None)
		instance.socio_id = socio_id.split(':')[0]
		# Grava dt_assembleia
		instance.dt_assembleia = datetime.datetime.strptime(data, '%d/%m/%Y').date()
		try:    # Vai tentar gravar a presença, em caso de erros de integridade dá erro
			instance.save()
			# Vai incrementar o nº de presenças e de representação na assembleia escolhida
			presencas = Assembleias.objects.filter(orgao=orgao, dt_assembleia=datetime.datetime.strptime(data, '%d/%m/%Y').date()).values('presencas')[0]['presencas']
			presencas += 1
			Assembleias.objects.filter(orgao=orgao, dt_assembleia=datetime.datetime.strptime(data, '%d/%m/%Y').date()).update(presencas=presencas)
			# Chama função para update das representações
			representacao = Decimal(request.POST.get('representacao', 0))
			update_reptassembly(orgao, datetime.datetime.strptime(data, '%d/%m/%Y').date(), representacao, '+')
			return HttpResponseRedirect(reverse('gestaugi:attendance'))
		except IntegrityError:
			messages.add_message(request, messages.INFO, 'Presença de sócio já registada para esta assembleia!')
			# return HttpResponseRedirect(reverse('gestaugi:dispmessage'))
			return render(request, 'gestaugi/messages.html', {'url': '/attendance'})
	else:
		print(form.errors)
	return render(request, 'gestaugi/newattendance.html', {
	  'form': form, 'socios' : socios, 'datas' : datas
	})

def load_dates(request):
	orgao = request.GET.get('orgao')
	datas = Assembleias.objects.filter(orgao=orgao).order_by('dt_assembleia')
	return render(request, 'gestaugi/load_dates.html', {'datas': datas})

def load_dates4edit(request,presenca_id):
	presenca = Presencas.objects.get(pk=presenca_id)
	orgao = request.GET.get('orgao')
	datas = Assembleias.objects.filter(orgao=orgao).order_by('dt_assembleia')
	dtselected = presenca.dt_assembleia
	return render(request, 'gestaugi/load_dates4edit.html', {'datas': datas, 'dtselected': dtselected})

def editattendance(request,presenca_id):
	presenca = Presencas.objects.get(pk=presenca_id)
	socios = Socios.objects.all().values('nsocio', 'nome').filter(pk=presenca.socio_id)
	datas = Assembleias.objects.all().values('dt_assembleia').order_by('dt_assembleia')
	dtselected = presenca.dt_assembleia
	form = PresencaForm(request.POST or None,instance=presenca)
	if form.is_valid():
		instance = form.save(commit=False)
		data = request.POST.get('data',None)
		# Vai buscar os dados originais a tabela
		olddata = Presencas.objects.filter(pk=presenca_id).values('dt_assembleia')[0]['dt_assembleia']
		oldorgao = Presencas.objects.filter(pk=presenca_id).values('orgao')[0]['orgao']
		oldrepresentacao = Presencas.objects.filter(pk=presenca_id).values('representacao')[0]['representacao']
        # Vai buscar os novos dados ao form - podem ser diferentes ou não
		newdata = datetime.datetime.strptime(data, '%d/%m/%Y').date()
		neworgao = request.POST.get('orgao', None)
		newrepresentacao = Decimal(request.POST.get('representacao', 0))
		# Chave estrangeira
		instance.socio_id = presenca.socio_id
		instance.dt_assembleia = datetime.datetime.strptime(data, '%d/%m/%Y').date()
		try:    # Vai tentar gravar a presença, em caso de erros de integridade dá erro
			instance.save()
			#Mesma assembleia, diferente representação
			if olddata == newdata and oldorgao == neworgao and oldrepresentacao != newrepresentacao:
				# Chama função para update das representações
				if oldorgao == 'AUGI':  # Para a associação não é preciso alterar
					# Anula a antiga representação
					update_reptassembly(oldorgao, olddata, oldrepresentacao, '-')
					# Adiciona a alterada
					update_reptassembly(oldorgao, olddata, newrepresentacao, '+')
				print(olddata)
				print(newdata)
				print(oldorgao)
				print(neworgao)
				print(oldrepresentacao)
				print(newrepresentacao)
			# Se houve alterações a data ou orgão -> Assembleia diferente
			if olddata != newdata or oldorgao != neworgao:
				# Vai diminuir o nº de presenças e de representação na assembleia anterior
				presencas = Assembleias.objects.filter(orgao=oldorgao, dt_assembleia=olddata).values('presencas')[0]['presencas']
				presencas -= 1
				Assembleias.objects.filter(orgao=oldorgao, dt_assembleia=olddata).update(presencas=presencas)
				# Anula a antiga representação
				update_reptassembly(oldorgao, olddata, oldrepresentacao, '-')
				# Vai aumentar o nº de presenças e de representação na assembleia escolhida
				presencas = Assembleias.objects.filter(orgao=neworgao, dt_assembleia=newdata).values('presencas')[0]['presencas']
				presencas += 1
				Assembleias.objects.filter(orgao=neworgao, dt_assembleia=newdata).update(presencas=presencas)
				# Adiciona a alterada
				update_reptassembly(neworgao, newdata, newrepresentacao, '+')
				print(olddata)
				print(newdata)
				print(oldorgao)
				print(neworgao)
				print(oldrepresentacao)
				print(newrepresentacao)
		except IntegrityError:
			messages.add_message(request, messages.INFO, 'Presença de sócio já registada para esta assembleia!')
			return render(request, 'gestaugi/messages.html', {'url': '/attendance'})
		return HttpResponseRedirect(reverse('gestaugi:attendance'))
	else:
		print(form.errors)
	return render(request, 'gestaugi/editattendance.html', {
	  'form': form, 'presenca' : presenca, 'socios' : socios, 'datas' : datas, 'dtselected' : dtselected
	})

def viewattendance(request,presenca_id):
	presenca = Presencas.objects.get(pk=presenca_id)
	socios = Socios.objects.all().values('nsocio', 'nome').filter(pk=presenca.socio_id)
	datas = Assembleias.objects.all().values('dt_assembleia').filter(dt_assembleia=presenca.dt_assembleia)
	form = PresencaViewForm(request.POST or None, instance=presenca)
	return render(request, 'gestaugi/viewattendance.html', {
	  'form': form, 'presenca' : presenca, 'socios' : socios, 'datas' : datas
	})

def deleteattendance(request,presenca_id):
	# Vai diminuir o nº de presenças e de representação na assembleia escolhida
	data = Presencas.objects.filter(pk=presenca_id).values('dt_assembleia')[0]['dt_assembleia']
	orgao = Presencas.objects.filter(pk=presenca_id).values('orgao')[0]['orgao']
	representacao = Presencas.objects.filter(pk=presenca_id).values('representacao')[0]['representacao']
	presencas = Assembleias.objects.filter(orgao=orgao, dt_assembleia=data).values('presencas')[0]['presencas']
	presencas -= 1
	Assembleias.objects.filter(orgao=orgao, dt_assembleia=data).update(presencas=presencas)
    # Suprime a presença
	instance = Presencas.objects.get(presenca_id=presenca_id)
	instance.delete()
	# Chama função para update das representações
	update_reptassembly(orgao,data,representacao,'-')
	return HttpResponseRedirect(reverse('gestaugi:attendance'))

def update_reptassembly(orgao,data,representacao,sinal):
	# Total areas dos socios presentes a dividir pela area total adquirida
	if orgao == 'AUGI':
		# Vai buscar a representação total / area total adquirida
		rept_total = Assembleias.objects.filter(orgao=orgao, dt_assembleia=data).values('rep_total')[0]['rep_total']
		# Vai buscar a representação dos socios presentes já registados
		rept_socios = Assembleias.objects.filter(orgao=orgao, dt_assembleia=data).values('rep_socios')[0]['rep_socios']
		# Adiciona a representação do sócio que está a ser registado
		if sinal == '+':
			rept_socios += representacao
		else:
			rept_socios -= representacao
		# Divide pela representação total e calcula o quorum
		rept_assembleia = rept_socios / rept_total
		# Faz o update da representação dos socios presentes
		Assembleias.objects.filter(orgao=orgao, dt_assembleia=data).update(rep_socios=rept_socios)
		# Faz o update da representação da assembleia
		Assembleias.objects.filter(orgao=orgao,dt_assembleia=data).update(rep_assembl=rept_assembleia)
	# Total socios presentes a dividir pelo total socios activos
	if orgao == 'Associação':
		# Vai buscar o total de sócios ativos / convocados
		rept_total = Assembleias.objects.filter(orgao=orgao, dt_assembleia=data).values('convocados')[0]['convocados']
		print(rept_total)
		# Vai buscar o numero de socios presentes já registados / o atual já foi registado antes
		rept_socios = Assembleias.objects.filter(orgao=orgao, dt_assembleia=data).values('presencas')[0]['presencas']
		print(rept_socios)
		# Divide pela representação total e calcula o quorum
		rept_assembleia = rept_socios / rept_total
		print(rept_assembleia)
		# Faz o update da representação da assembleia
		Assembleias.objects.filter(orgao=orgao,dt_assembleia=data).update(rep_assembl=rept_assembleia)


def expenses_page_view(request):
	despesas = Despesas.objects.all().order_by("despesa_id")
	filtro = DespesasFilter(request.GET,despesas)
	table = DespesasTable(filtro.qs)
	table.paginate(page=request.GET.get("page", 1), per_page=10)
	return render(request, 'gestaugi/expenses.html',
				  context={"model":despesas, "table":table, "filter": filtro})

def newexpense(request):
	#Lista de socios para escolha / associar a despesa
	tdespesas = TiposDespesas.objects.all().values('tipo_id','descricao').order_by('tipo_id')
	form = DespesasForm(request.POST or None, initial={'dt_registo': datetime.date.today()})
	if form.is_valid():
		instance = form.save(commit=False)
		instance.tipo_id = request.POST.get('tdespesa', None)
		if (instance.tipo_id == 'Escolha tipo...'):
			messages.add_message(request, messages.INFO,'Tem de escolher um tipo de despesa!')
			return render(request, 'gestaugi/messages.html', {'url': '/newexpense'})
		else:
			instance.save()
		return HttpResponseRedirect(reverse('gestaugi:expenses'))
	else:
		print(form.errors)
		#form = DespesasForm()
	return render(request, 'gestaugi/newexpense.html', {
	  'form': form, 'tdespesas' : tdespesas
	})

def editexpense(request,despesa_id):
	despesa = Despesas.objects.get(pk=despesa_id)
	# Id do Tipo de Despesa
	tipo_id = Despesas.objects.get(pk=despesa_id).tipo_id
	# Vai buscar a descrição do Tipo de Despesa, vai ficar selecionado no dropdown
	tdespesa = TiposDespesas.objects.all().values('tipo_id', 'descricao').filter(pk=tipo_id)
	form = DespesasForm(request.POST or None, instance=despesa)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaugi:expenses'))
	return render(request, 'gestaugi/editexpense.html', {
	  'form': form, 'tdespesa' : tdespesa, 'despesa' : despesa
	})

def viewexpense(request,despesa_id):
	despesa = Despesas.objects.get(pk=despesa_id)
	# Id do Tipo de Despesa
	tipo_id = Despesas.objects.get(pk=despesa_id).tipo_id
	# Vai buscar a descrição do Tipo de Despesa, vai ficar selecionado no dropdown
	tdespesa = TiposDespesas.objects.all().values('tipo_id', 'descricao').filter(pk=tipo_id)
	form = DespesasViewForm(request.POST or None, instance=despesa)
	return render(request, 'gestaugi/viewexpense.html', {
	  'form': form, 'tdespesa' : tdespesa, 'despesa' : despesa
	})

def deletexpense(request,despesa_id):
	instance = Despesas.objects.get(despesa_id=despesa_id)
	instance.delete()
	return HttpResponseRedirect(reverse('gestaugi:expenses'))

def annuities_page_view(request):
	anuidades = Anuidades.objects.all().order_by("anuidade_id")
	filtro = AnuidadesFilter(request.GET,anuidades)
	table = AnuidadesTable(filtro.qs)
	table.paginate(page=request.GET.get("page", 1), per_page=10)
	return render(request, 'gestaugi/annuities.html',
				  context={"model":anuidades, "table":table, "filter": filtro})

def newannuity(request):
	#Lista de socios para escolha / associar a anuidade
	socios = Socios.objects.all().values('socio_id','nsocio','nome').order_by('nome')
	form = AnuidadesForm(request.POST or None,initial={"anuidade": 30})
	if form.is_valid():
		instance = form.save(commit=False)
		socio_id = request.POST.get('socio', None)
		if (socio_id == 'Escolha sócio...'):
			messages.add_message(request, messages.INFO,'Tem de escolher um sócio!')
			return render(request, 'gestaugi/messages.html', {'url': '/newannuity'})
		else:
			instance.socio_id = socio_id
			# Vai buscar o valor de anuidade que o sócio tem em divida
			anuidivida = Socios.objects.filter(pk=socio_id).values('anuidivida')[0]['anuidivida']
			# Adiciona o novo valor de comparticipação
			anuidivida = anuidivida + Decimal(request.POST.get('anuidade', 0))
			instance.save()
			# Regista na tabela de Sócios o novo valor de anuidade em divida
			Socios.objects.filter(pk=socio_id).update(anuidivida=anuidivida)
			return HttpResponseRedirect(reverse('gestaugi:annuities'))
	else :
		print(form.errors)
		#form = AnuidadesForm()
	return render(request, 'gestaugi/newannuity.html', {
	  'form': form, 'socios' : socios
	})

def editannuity(request,anuidade_id):
	anuidade = Anuidades.objects.get(pk=anuidade_id)
	# Se anuidade é alterada o valor anterior precisa de ser anulado
	valor_anterior = anuidade.anuidade
	# Id do Socio associado a anuidade
	socio_id = Anuidades.objects.get(pk=anuidade_id).socio_id
	# Vai buscar o nome do Socio a tabela de sócios, vai ficar selecionado no dropdown
	socios = Socios.objects.all().values('nsocio', 'nome').filter(pk=socio_id)
	form = AnuidadesForm(request.POST or None, instance=anuidade)
	if form.is_valid():
		# Vai buscar o valor de anuidade que o sócio tem em divida
		anuidivida = Socios.objects.filter(pk=socio_id).values('anuidivida')[0]['anuidivida']
		# Retira valor anterior
		anuidivida = anuidivida - valor_anterior
		# Adiciona o novo valor de anuidade
		anuidivida = anuidivida + Decimal(request.POST.get('anuidade', 0))
		# Guarda os dados do form
		form.save()
		# Regista na tabela de Sócios o novo valor de anuidade em divida
		Socios.objects.filter(pk=socio_id).update(anuidivida=anuidivida)
		return HttpResponseRedirect(reverse('gestaugi:annuities'))
	return render(request, 'gestaugi/editannuity.html', {
	  'form': form, 'socios' : socios, 'anuidade' : anuidade,
	})

def viewannuity(request,anuidade_id):
	anuidade = Anuidades.objects.get(pk=anuidade_id)
	# Id do Socio associado a anuidade
	socio_id = Anuidades.objects.get(pk=anuidade_id).socio_id
	# Vai buscar o nome do Socio a tabela de sócios, vai ficar selecionado no dropdown
	socios = Socios.objects.all().values('nsocio', 'nome').filter(pk=socio_id)
	form = AnuidadesViewForm(request.POST or None, instance=anuidade)
	return render(request, 'gestaugi/viewannuity.html', {
	   'form': form, 'socios' : socios, 'anuidade' : anuidade,
	})

def deleteannuity(request,anuidade_id):
	instance = Anuidades.objects.get(anuidade_id=anuidade_id)
	# Se anuidade é suprimida o valor precisa de ser anulado no registo do sócio
	valor_anterior = instance.anuidade
	socio_id = instance.socio_id
	# Vai buscar o valor em divida no registo do sócio
	anuidivida = Socios.objects.filter(pk=socio_id).values('anuidivida')[0]['anuidivida']
	# E retira o valor a suprimir
	anuidivida = anuidivida - valor_anterior
	instance.delete()
	# Regista na tabela de Sócios o valor de anuidades em divida atualizado
	Socios.objects.filter(pk=socio_id).update(anuidivida=anuidivida)
	return HttpResponseRedirect(reverse('gestaugi:annuities'))

def payments_page_view(request):
	pagamentos = Pagamentos.objects.all().order_by("pagamento_id")
	filtro = PagamentosFilter(request.GET,pagamentos)
	table = PagamentosTable(filtro.qs)
	table.paginate(page=request.GET.get("page", 1), per_page=10)
	return render(request, 'gestaugi/payments.html',
				  context={"model":pagamentos, "table":table, "filter": filtro})

def newpayment(request):
	#Lista de socios para escolha / associar a anuidade
	socios = Socios.objects.all().values('socio_id','nsocio','nome').order_by('nome')
	#Lista de lotes para escolha
	lotes = Lotes.objects.all()
	form = PagamentosForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.socio_id = request.POST.get('socio', None)
		socio_id = request.POST.get('socio', None)
		if (socio_id == 'Escolha sócio...'):
			messages.add_message(request, messages.INFO,'Tem de escolher um sócio!')
			return render(request, 'gestaugi/messages.html', {'url': '/newpayment'})
		else:
			# Vai verificar o tipo de pagamento
			tipopag = request.POST.get('tipo', None)
			if tipopag == 'Anuidade':
				# Vai buscar o valor de anuidade que o sócio tem em divida
				anuidivida = Socios.objects.filter(pk=socio_id).values('anuidivida')[0]['anuidivida']
				# Subtrai ao valor em didiva o valor do pagamento
				anuidivida = anuidivida - int(request.POST.get('pagamento', 0))
				# Regista na tabela de Sócios o novo valor de anuidade em divida
				Socios.objects.filter(pk=socio_id).update(anuidivida=anuidivida)
			else:    # Pagamentos de comparticipações ou despesas
				# Vai buscar o valor de comparticipação que o sócio tem em divida
				compdivida = Socios.objects.filter(pk=socio_id).values('compdivida')[0]['compdivida']
				# Subtrai ao valor em didiva o valor do pagamento
				compdivida = compdivida - int(request.POST.get('pagamento', 0))
				# Regista na tabela de Sócios o novo valor de comparticipação em divida
				Socios.objects.filter(pk=socio_id).update(compdivida=compdivida)
				if tipopag == 'Comparticipação':
					# Se comparticipação regista nº de lote
					instance.lote_id = request.POST.get('lote', None)
			# Grava os dados do form
			instance.save()
			return HttpResponseRedirect(reverse('gestaugi:payments'))
	else :
		print(form.errors)
		#form = PagamentosForm()
	return render(request, 'gestaugi/newpayment.html', {
	  'form': form, 'socios' : socios, 'lotes' : lotes
	})

def editpayment(request,pagamento_id):
	pagamento = Pagamentos.objects.get(pk=pagamento_id)
	# Se o pagamento é alterada o valor anterior precisa de ser anulado
	valor_anterior = pagamento.pagamento
	# Id do Socio associado a anuidade
	socio_id = Pagamentos.objects.get(pk=pagamento_id).socio_id
	# Vai buscar o nome do Socio a tabela de sócios, vai ficar selecionado no dropdown
	socios = Socios.objects.all().values('nsocio', 'nome').filter(pk=socio_id)
	# Vai buscar o lote
	lote = Lotes.objects.all().filter(pk=pagamento.lote_id)
	form = PagamentosForm(request.POST or None, instance=pagamento)
	if form.is_valid():
		# Vai buscar o valor de comparticipação que o sócio tem em divida
		compdivida = Socios.objects.filter(pk=socio_id).values('compdivida')[0]['compdivida']
		# Anula o valor anterior do pagamento
		compdivida = compdivida + valor_anterior
		# Subtrai ao valor em didiva o valor do pagamento
		compdivida = compdivida - Decimal(request.POST.get('pagamento', 0))
		form.save()
		# Regista na tabela de Sócios o novo valor de comparticipação em divida
		Socios.objects.filter(pk=socio_id).update(compdivida=compdivida)
		return HttpResponseRedirect(reverse('gestaugi:payments'))
	return render(request, 'gestaugi/editpayment.html', {
	  'form': form, 'socios' : socios, 'pagamento' : pagamento, 'lote' : lote
	})

def viewpayment(request,pagamento_id):
	pagamento = Pagamentos.objects.get(pk=pagamento_id)
	# Id do Socio associado ao pagamento
	socio_id = Pagamentos.objects.get(pk=pagamento_id).socio_id
	# Vai buscar o nome do Socio a tabela de sócios, vai ficar selecionado no dropdown
	socios = Socios.objects.all().values('nsocio', 'nome').filter(pk=socio_id)
	# Vai buscar o lote
	lote = Lotes.objects.all().filter(pk=pagamento.lote_id)
	form = PagamentosViewForm(request.POST or None, instance=pagamento)
	return render(request, 'gestaugi/viewpayment.html', {
	   'form': form, 'socios' : socios, 'pagamento' : pagamento, 'lote' : lote
	})

def deletepayment(request,pagamento_id):
	instance = Pagamentos.objects.get(pagamento_id=pagamento_id)
	# Se pagamento é suprimido o valor precisa de ser anulado no registo do sócio
	valor_anterior = instance.pagamento
	socio_id = instance.socio_id
	# Verifica qual o tipo de pagamento
	tipo = instance.tipo
	if tipo == "Anuidade":
		# Vai buscar o valor em divida no registo do sócio
		anuidivida = Socios.objects.filter(pk=socio_id).values('anuidivida')[0]['anuidivida']
		# E retira o valor a suprimir
		anuidivida = anuidivida + valor_anterior
		# Regista na tabela de Sócios o valor de anuidades em divida atualizado
		Socios.objects.filter(pk=socio_id).update(anuidivida=anuidivida)
	else:
		# Vai buscar o valor em divida no registo do sócio
		compdivida = Socios.objects.filter(pk=socio_id).values('compdivida')[0]['compdivida']
		# E retira o valor a suprimir
		compdivida = compdivida + valor_anterior
		# Regista na tabela de Sócios o valor de comparticipações em divida atualizado
		Socios.objects.filter(pk=socio_id).update(compdivida=compdivida)
	instance.delete()
	# Se o pagamento for suprimido o valor em divida na tabela de sócios precisa de ser atualizado
	return HttpResponseRedirect(reverse('gestaugi:payments'))

def reports(request):
	return render(request, 'gestaugi/reports.html')

def listpartners2pdf(request):
    template_name = "listpartners.html"
    socios = Socios.objects.all().order_by("nsocio")
    return save2pdf(
        template_name, "Socios.pdf", {"record": socios, }
    )

def listpartners2csv(request):
    socios = Socios.objects.all().order_by("nsocio")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=lista_socios.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=";")
    writer.writerow(['Nº', 'Nome','Lotes', 'Morada', 'Localidade','Telemovel', 'Email','Estado'])
    for linha in socios:
        writer.writerow([linha.nsocio,linha.nome,linha.lotes, linha.morada,linha.localidade, linha.telemovel,
						 linha.email, linha.estado])
    return response

def listdebts2pdf(request):
    template_name = "listdebts.html"
    dividas = Socios.objects.raw(sql_debts)
    return save2pdf(
        template_name, "Dividas_Socios.pdf", {"record": dividas, }
    )

def listdebts2csv(request):
   dividas = Socios.objects.raw(sql_debts)
   response = HttpResponse(content_type='text/csv')
   response['Content-Disposition'] = 'attachment; filename=dividas.csv'
   response.write(u'\ufeff'.encode('utf8'))
   writer = csv.writer(response, delimiter=";")
   writer.writerow(['NºSócio', 'Nome', 'Lotes', 'Anuidades Divida','Compart. Divida', 'Compart. Pagas','Estado'])
   for linha in dividas:
      writer.writerow([linha.nsocio, linha.nome,linha.lotes, linha.anuidivida ,linha.compdivida, linha.compartpag, linha.estado])
   return response

def listcomparts2pdf(request):
    template_name = "listcomparts.html"
    compart = Comparticipacoes.objects.select_related('socio').all()
    return save2pdf(
        template_name, "Comparticipacoes.pdf", {"record": compart, }
    )

def listcomparts2csv(request):
    compart = Comparticipacoes.objects.select_related('socio').all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=comparticipacoes.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=";")
    writer.writerow(['NºSócio', 'Nome', 'Comparticipação', 'Descrição','Dt. Valor'])
    for linha in compart:
        writer.writerow([linha.socio.nsocio,linha.socio.nome,linha.valor_calculado,linha.descricao,linha.dt_valor])
    return response

def listpayments2pdf(request):
    template_name = "listpayments.html"
    pagamentos = Pagamentos.objects.select_related('socio').all()
    return save2pdf(
        template_name, "Pagamentos.pdf", {"record": pagamentos, }
    )

def listpayments2csv(request):
    pagamentos = Pagamentos.objects.select_related('socio').all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=pagamentos.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=";")
    writer.writerow(['NºSócio', 'Nome', 'Pagamento','Tipo', 'Descrição','Dt. Pagamento'])
    for linha in pagamentos:
        writer.writerow([linha.socio.nsocio,linha.socio.nome,linha.pagamento,linha.tipo,linha.descricao,linha.dt_pagamento])
    return response

def listtotpayments2pdf(request):
    template_name = "listtotpayments.html"
    pagamentos = Pagamentos.objects.raw(sql_payments)
    return save2pdf(
        template_name, "Total_Pagamentos.pdf", {"record": pagamentos, }
    )

def listtotpayments2csv(request):
    pagamentos = Pagamentos.objects.raw(sql_payments)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=pagamentos_totais.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=";")
    writer.writerow(['NºSócio', 'Nome', 'Anuidades Pagas','Comparticipações Pagas'])
    for linha in pagamentos:
        writer.writerow([linha.socio.nsocio,linha.socio.nome,linha.anuidades,linha.comparticipacoes])
    return response

def listexpenses2pdf(request):
    template_name = "listexpenses.html"
    despesas = Despesas.objects.raw(sql_expenses)
    return save2pdf(
        template_name, "Despesas.pdf", {"record": despesas, }
    )

def listexpenses2csv(request):
    despesas = Despesas.objects.raw(sql_expenses)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=despesas.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=";")
    writer.writerow(['Descrição', 'Ano', 'Despesa','Dt. Registo'])
    for linha in despesas:
        writer.writerow([linha.descricao,linha.ano,linha.despesa,linha.dt_registo])
    return response

def listotexpenses2pdf(request):
    template_name = "listotexpenses.html"
    despesas = Despesas.objects.raw(sql_totexpenses)
    return save2pdf(
        template_name, "Despesas_Totais.pdf", {"record": despesas, }
    )

def listotexpenses2csv(request):
    despesas = Despesas.objects.raw(sql_totexpenses)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=despesas_totais.csv'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=";")
    writer.writerow(['Descrição', 'Despesa'])
    for linha in despesas:
        writer.writerow([linha.descricao,linha.despesa])
    return response

def settings(request):
	return render(request, 'gestaugi/settings.html')

def expensestypes_page_view(request):
	tdespesas = TiposDespesas.objects.all().order_by("tipo_id")
	filtro = TDespesasFilter(request.GET,tdespesas)
	table = TDespesasTable(filtro.qs)
	table.paginate(page=request.GET.get("page", 1), per_page=10)
	return render(request, 'gestaugi/expensestypes.html',
				  context={"model":tdespesas, "table":table, "filter": filtro})

def newexpensetype(request):
	form = TiposDespesasForm(request.POST or None)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaugi:expensestypes'))
	else:
		print(form.errors)
		#form = DespesasForm()
	return render(request, 'gestaugi/newexpensetype.html', {
	  'form': form
	})

def editexpensetype(request,tipo_id):
	tdespesa = TiposDespesas.objects.get(pk=tipo_id)
	form = TiposDespesasForm(request.POST or None, instance=tdespesa)
	if form.is_valid():
		form.save()
		return HttpResponseRedirect(reverse('gestaugi:expensestypes'))
	return render(request, 'gestaugi/editexpensetype.html', {
	  'form': form, 'tipo_id' : tipo_id
	})

def viewexpensetype(request,tipo_id):
	tdespesa = TiposDespesas.objects.get(pk=tipo_id)
	form = TiposDespesasViewForm(request.POST or None, instance=tdespesa)
	return render(request, 'gestaugi/viewexpensetype.html', {
	  'form': form, 'tipo_id' : tipo_id
	})

def deletexpensetype(request,tipo_id):
	instance = TiposDespesas.objects.get(tipo_id=tipo_id)
	try:
		instance.delete()
		return HttpResponseRedirect(reverse('gestaugi:expensestypes'))
	except ProtectedError:
		messages.add_message(request, messages.INFO, 'Tipo de Despesa já usado na tabela de Despesas. Não é possivel suprimir!')
		#return HttpResponseRedirect(reverse('gestaugi:dispmessage'))
		return render(request,'gestaugi/messages.html',{'url':'/expensestypes'})


def dashboard(request):
    return render(request, 'gestaugi/dashboard.html')

def expensesbytype(request):
	labels = []
	data = []
	queryset = Despesas.objects.values('tipo__descricao').annotate(tipo_despesa=Sum('despesa')).order_by('-tipo_despesa')
	for entry in queryset:
		labels.append(entry['tipo__descricao'])
		data.append(entry['tipo_despesa'])

	return JsonResponse(data={
		'labels': labels,
		'data': data,
	})

def dispmessage(request):
	return render(request, 'gestaugi/messages.html')

def parameters_page_view(request):
	parametros = Parametros.objects.all().filter(pk=1)
	table =  ParametrosTable(parametros)
	table.paginate(page=request.GET.get("page", 1), per_page=10)
	return render(request, 'gestaugi/parameters.html',
				  context={"table":table})

def divdashboard_page_view(request):
	return render(request, 'gestaugi/divdashboard.html')

def infodashboard(request):
	labels = []
	data = []
	queryset = AugiDashboard.objects.values('municipio').annotate(numero=Sum('numero')).order_by('-numero')
	for entry in queryset:
		labels.append(entry['municipio'])
		data.append(entry['numero'])

	return JsonResponse(data={
		'labels': labels,
		'data': data,
	})

def divdashboard2_page_view(request):
	return render(request, 'gestaugi/divdashboard2.html')

def infodashboard2(request):
	labels = []
	data = []
	queryset = AugiDashboard.objects.filter(reconversao__gt=0).values('municipio').annotate(reconversao=Sum('reconversao')).order_by('-reconversao')
	for entry in queryset:
		labels.append(entry['municipio'])
		data.append(entry['reconversao'])

	return JsonResponse(data={
		'labels': labels,
		'data': data,
	})

def divdashboard3_page_view(request):
	return render(request, 'gestaugi/divdashboard3.html')

def infodashboard3(request):
	labels = []
	data = []
	queryset = AugiDashboard.objects.filter(reconversao__gt=0).values('municipio').annotate(area_total=Sum('area_total')).order_by('-area_total')
	for entry in queryset:
		labels.append(entry['municipio'])
		data.append(entry['area_total'])

	return JsonResponse(data={
		'labels': labels,
		'data': data,
	})

def divdashboard4_page_view(request):
	return render(request, 'gestaugi/divdashboard4.html')

def infodashboard4(request):
	labels = []
	data = []
	queryset = AugiDashboard.objects.filter(reconversao__gt=0).values('municipio').annotate(area_media=Sum('area_media')).order_by('area_media')
	for entry in queryset:
		labels.append(entry['municipio'])
		data.append(entry['area_media'])

	return JsonResponse(data={
		'labels': labels,
		'data': data,
	})

def divdashboard5_page_view(request):
	return render(request, 'gestaugi/divdashboard5.html')

def infodashboard5(request):
	labels = []
	data = []
	queryset = AugiDashboard.objects.filter(reconversao__gt=0).values('municipio').annotate(augi_maior=Sum('augi_maior'))
	for entry in queryset:
		labels.append(entry['municipio'])
		data.append(entry['augi_maior'])

	return JsonResponse(data={
		'labels': labels,
		'data': data,
	})