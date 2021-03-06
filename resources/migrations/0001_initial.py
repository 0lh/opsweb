# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-11 10:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=10, unique=True, verbose_name='idc 字母简称')),
                ('idc_name', models.CharField(default='', max_length=100, verbose_name='idc 中文名称')),
                ('address', models.CharField(max_length=255, null=True, verbose_name='具体地址,云厂商可以不填')),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='机房联系电话')),
                ('email', models.EmailField(default='', max_length=32, null=True, verbose_name='机房联系邮件')),
                ('username', models.CharField(max_length=32, null=True, verbose_name='机房联系人')),
            ],
            options={
                'db_table': 'resources_idc',
            },
        ),
    ]
