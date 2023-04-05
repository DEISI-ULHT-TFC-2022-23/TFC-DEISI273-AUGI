from django.db import models

# Create your models here.

class CodPostais(models.Model):
    codpostal = models.CharField(primary_key=True,max_length=10,verbose_name="Cod.Postal")
    localidade = models.CharField(max_length=50,verbose_name="Localidade")

    def __str__(self):
        return f"{self.codpostal}"

class Socios(models.Model):
    socio_id = models.AutoField(primary_key=True,verbose_name="ID")
    nsocio = models.IntegerField(default=0,unique=True, verbose_name="NºSócio")
    nome = models.CharField(max_length=80,verbose_name="Sócio")
    morada = models.CharField(max_length=80)
    localidade = models.CharField(max_length=80, verbose_name="Localidade")
    cpostal = models.ForeignKey(CodPostais,on_delete=models.PROTECT, related_name="Codpost",verbose_name="Cod.Postal")
    cpostlocal = models.CharField(max_length=80, verbose_name="Local.Cod.Post")
    telemovel = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    lotes = models.CharField(max_length=80, verbose_name="Lotes")
    compdivida = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Comp. Devidas")
    anuidivida = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Anuid. Devidas")
    dt_admissao = models.DateField(verbose_name="Dt.Admissão")
    estado = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.socio_id}"

class Lotes(models.Model):
    lote_id = models.AutoField(primary_key=True,verbose_name="ID Lote")
    nlote = models.IntegerField(default=0,verbose_name="NºLote")
    socio = models.ForeignKey(Socios,on_delete=models.PROTECT, related_name="Socios",verbose_name="NºSocio")
    area = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    local = models.CharField(max_length=80)
    dt_aquisicao = models.DateField(verbose_name="Dt.Aquisição")
    dt_venda = models.DateField(null=True, blank=True,verbose_name="Dt.Venda")
    nfogos = models.IntegerField(default=0,verbose_name="NºFogos")
    frenteslote = models.IntegerField(default=0,verbose_name="Frentes Lote")

    def __str__(self):
        return f"{self.lote_id}"

class Comparticipacoes(models.Model):
    compart_id = models.AutoField(primary_key=True,verbose_name="ID.Comparticipação")
    lote = models.ForeignKey(Lotes,on_delete=models.PROTECT, related_name="LotesComp",verbose_name="ID Lote")
    socio = models.ForeignKey(Socios,on_delete=models.PROTECT, related_name="SociosComp",verbose_name="ID Socio")
    valor_calculado = models.DecimalField(max_digits=12, decimal_places=2, default=0,verbose_name="Valor")
    descricao = models.CharField(max_length=80,verbose_name="Descrição")
    tipo = models.CharField(max_length=80,verbose_name="Tipo")
    dt_valor = models.DateField(verbose_name="Dt.Valor")
    dt_registo = models.DateField(verbose_name="Dt.Registo")
    estado = models.CharField(max_length=15,verbose_name="Estado")   # Paga, paga parcialmente, não paga
    dt_estado = models.DateField(default=0,verbose_name="Data")

    def __str__(self):
        return f"{self.compart_id}"

class Pagamentos(models.Model):
    pagamento_id = models.AutoField(primary_key=True, verbose_name="ID.Pagamento")
    socio = models.ForeignKey(Socios,on_delete=models.PROTECT, related_name="SociosPag",verbose_name="ID Socio")
    pagamento = models.DecimalField(max_digits=12, decimal_places=2, default=0,verbose_name="Pagamento")        # V
    tipo = models.CharField(max_length=80,verbose_name="Tipo")
    lote = models.ForeignKey(Lotes, on_delete=models.PROTECT, related_name="LotesPag",blank=True, null=True ,verbose_name="ID Lote")
    descricao = models.CharField(max_length=80,verbose_name="Descrição")
    dt_pagamento = models.DateField(verbose_name="Dt.Pagamento")

    def __str__(self):
        return f"{self.pagamento_id}"

class Assembleias(models.Model):
    assembleia_id = models.AutoField(primary_key=True,verbose_name="ID.Assembleia")
    tipo = models.CharField(max_length=20,verbose_name="Tipo")
    orgao = models.CharField(max_length=20,verbose_name="Orgão")
    cpostal = models.CharField(max_length=10,verbose_name="Cod.Postal")
    localidade = models.CharField(max_length=80, verbose_name="Localidade")
    dt_assembleia = models.DateField(verbose_name="Dt.Assembleia")
    convocados = models.IntegerField(default=0, verbose_name="Convocados")
    presencas = models.IntegerField(default=0, verbose_name="Presenças")
    rep_total = models.DecimalField(max_digits=12, decimal_places=2, default=0,verbose_name="Representação Total")
    rep_socios = models.DecimalField(max_digits=12, decimal_places=2, default=0,verbose_name="Representação Sócios")
    rep_assembl = models.DecimalField(max_digits=12, decimal_places=2,default=0,verbose_name="Representação Assembleia")

    def __str__(self):
        return f"{self.assembleia_id}"

class Presencas(models.Model):
    presenca_id = models.AutoField(primary_key=True,verbose_name="ID.Presença")
    socio = models.ForeignKey(Socios,on_delete=models.PROTECT, related_name="SociosPres",verbose_name="Socio")
    orgao = models.CharField(max_length=20,verbose_name="Orgão")
    dt_assembleia = models.DateField(verbose_name="Dt.Assembleia")
    representacao = models.DecimalField(max_digits=12, decimal_places=2, default=0,verbose_name="Representação")

    class Meta:
        unique_together = ('socio', 'orgao','dt_assembleia')

    def __str__(self):
        return f"{self.presenca_id}"

class TiposDespesas(models.Model):
    tipo_id = models.AutoField(primary_key=True,verbose_name="Id.Tipo")
    descricao = models.CharField(max_length=80,verbose_name="Descrição")

    def __str__(self):
        return f"{self.tipo_id}"

class Despesas(models.Model):
    despesa_id = models.AutoField(primary_key=True,verbose_name="Id.Despesa")
    tipo = models.ForeignKey(TiposDespesas, on_delete=models.PROTECT, related_name="TDespesas", verbose_name="Tipo")
    despesa = models.DecimalField(max_digits=12, decimal_places=2,default=0,verbose_name="Despesa")
    ano = models.IntegerField(default=0, verbose_name="Ano")
    descricao = models.CharField(max_length=80,verbose_name="Descrição")
    dt_registo = models.DateField(verbose_name="Dt.Registo")

    def __str__(self):
        return f"{self.despesa_id}"

class Anuidades(models.Model):
    anuidade_id = models.AutoField(primary_key=True,verbose_name="Id.Anuidade")
    socio = models.ForeignKey(Socios, on_delete=models.PROTECT, related_name="SociosAnu", verbose_name="ID Socio")
    anuidade = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Anuidade")
    ano = models.IntegerField(default=0, verbose_name="Ano")
    dt_pagamento = models.DateField(null=True, blank=True,verbose_name="Dt.Pagamento")

    def __str__(self):
        return f"{self.anuidade_id}"

class Parametros(models.Model):
    param_id = models.AutoField(primary_key=True,verbose_name="Id.Parametro")
    vtotobra = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="V.Tot.Obra")
    tfrenlot = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="T.Frentes Lote")
    tfoglot = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="T.Fogos Lote")
    tarealot = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="T.Areas Lote")

    def __str__(self):
        return f"{self.param_id}"