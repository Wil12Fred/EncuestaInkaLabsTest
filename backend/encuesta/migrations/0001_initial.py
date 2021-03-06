# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-10-28 15:40
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alternativa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Alternativa_orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.IntegerField()),
                ('total', models.IntegerField()),
                ('alternativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.Alternativa')),
            ],
        ),
        migrations.CreateModel(
            name='Encuesta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('descripción', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Encuesta_alternativa_orden',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='EncuestaPregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.Encuesta')),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('enunciado', models.CharField(max_length=50)),
                ('tipo', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(2), django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Pregunta_detalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.Alternativa')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.Pregunta')),
            ],
        ),
        migrations.CreateModel(
            name='Solucion_alternativa_detalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternativa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.Alternativa')),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.EncuestaPregunta')),
            ],
        ),
        migrations.CreateModel(
            name='Solucion_alternativa_orden_detalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternativas', models.ManyToManyField(through='encuesta.Encuesta_alternativa_orden', to='encuesta.Alternativa_orden')),
            ],
        ),
        migrations.CreateModel(
            name='Solucion_texto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=30)),
                ('count', models.IntegerField(default=1)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.EncuestaPregunta')),
            ],
        ),
        migrations.CreateModel(
            name='Solucion_texto_detalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.CharField(max_length=50)),
                ('pregunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.EncuestaPregunta')),
            ],
        ),
        migrations.AddField(
            model_name='pregunta',
            name='alternativas',
            field=models.ManyToManyField(blank=True, through='encuesta.Pregunta_detalle', to='encuesta.Alternativa'),
        ),
        migrations.AddField(
            model_name='encuestapregunta',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.Pregunta'),
        ),
        migrations.AddField(
            model_name='encuesta_alternativa_orden',
            name='Solucion_alternativa_orden_detalle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.Solucion_alternativa_orden_detalle'),
        ),
        migrations.AddField(
            model_name='encuesta_alternativa_orden',
            name='alternativa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.Alternativa_orden'),
        ),
        migrations.AddField(
            model_name='encuesta',
            name='preguntas',
            field=models.ManyToManyField(blank=True, through='encuesta.EncuestaPregunta', to='encuesta.Pregunta'),
        ),
        migrations.AddField(
            model_name='alternativa_orden',
            name='pregunta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encuesta.EncuestaPregunta'),
        ),
        migrations.AlterUniqueTogether(
            name='pregunta_detalle',
            unique_together=set([('pregunta', 'alternativa')]),
        ),
        migrations.AlterUniqueTogether(
            name='encuestapregunta',
            unique_together=set([('encuesta', 'pregunta')]),
        ),
        migrations.AlterUniqueTogether(
            name='alternativa_orden',
            unique_together=set([('pregunta', 'alternativa', 'orden')]),
        ),
    ]
