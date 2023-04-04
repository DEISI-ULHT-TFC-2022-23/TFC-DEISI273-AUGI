# Generated by Django 4.1.3 on 2023-03-18 19:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestaugi', '0002_alter_anuidades_socio_alter_comparticipacoes_lote_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagamentos',
            fields=[
                ('pagamento_id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID.Pagamento')),
                ('pagamento', models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Pagamento')),
                ('tipo', models.CharField(max_length=80, verbose_name='Tipo')),
                ('descricao', models.CharField(max_length=80, verbose_name='Descrição')),
                ('dt_pagamento', models.DateField(verbose_name='Dt.Pagamento')),
                ('socio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='SociosPag', to='gestaugi.socios', verbose_name='ID Socio')),
            ],
        ),
    ]
