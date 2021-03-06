# Generated by Django 4.0.1 on 2022-01-18 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carro',
            fields=[
                ('placa', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('marca', models.CharField(max_length=10)),
                ('modelo', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Estacionamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horaDeEntrada', models.DateTimeField()),
                ('horaDeSaida', models.DateTimeField()),
                ('placaVeiculo', models.CharField(max_length=8)),
                ('valor', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Vaga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocupado', models.BooleanField(default=False)),
                ('carro', models.ForeignKey(default=0, null=True, on_delete=django.db.models.deletion.RESTRICT, to='app.carro')),
                ('estacionamento', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.estacionamento')),
            ],
        ),
    ]
