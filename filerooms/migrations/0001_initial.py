# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filerooms.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='file name')),
                ('description', models.TextField(verbose_name='description')),
                ('attachment', filerooms.fields.ProtectedStorageFileField(upload_to='')),
                ('created', models.DateTimeField(null=True, verbose_name='created date', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('slug', models.SlugField(unique=True, verbose_name='slug', blank=True)),
                ('is_public', models.BooleanField(default=False, help_text='If this room is made public, then anyone can see the files in it', verbose_name='public room')),
                ('owners', models.ManyToManyField(related_name='rooms', verbose_name='owners', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='download',
            name='room',
            field=models.ForeignKey(related_name='downloads', verbose_name='file room', to='filerooms.Room'),
            preserve_default=True,
        ),
    ]
