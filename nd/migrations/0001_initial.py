# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cause',
            fields=[
                ('text', models.CharField(max_length=200, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='DTC',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('bmw_code', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Phrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('file', models.CharField(max_length=200)),
                ('page', models.IntegerField()),
            ],
        ),
        migrations.AddIndex(
            model_name='phrase',
            index=models.Index(fields=[b'text'], name='nd_phrase_text_f0288e_idx'),
        ),
        migrations.AddIndex(
            model_name='phrase',
            index=models.Index(fields=[b'file'], name='nd_phrase_file_8a00b0_idx'),
        ),
        migrations.AddIndex(
            model_name='phrase',
            index=models.Index(fields=[b'page'], name='nd_phrase_page_9edf8d_idx'),
        ),
        migrations.AddField(
            model_name='dtc',
            name='causes',
            field=models.ManyToManyField(to='nd.Cause'),
        ),
    ]
