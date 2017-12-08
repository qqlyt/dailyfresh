# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('df_goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsinfo',
            name='gclick',
            field=models.IntegerField(default=21),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gcontent',
            field=tinymce.models.HTMLField(default=b'\xe5\x86\x85\xe5\xae\xb9'),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gprice',
            field=models.DecimalField(default=10, max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gprofile',
            field=models.CharField(default=b'\xe7\xae\x80\xe4\xbb\x8b', max_length=200),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gstock',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='goodsinfo',
            name='gtitle',
            field=models.CharField(default=b'\xe6\xa2\xa8\xe5\xad\x90\xe5\x8f\xb7', max_length=20),
        ),
    ]
