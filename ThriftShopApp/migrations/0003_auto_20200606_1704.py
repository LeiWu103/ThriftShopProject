# Generated by Django 2.1.13 on 2020-06-06 09:04

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ThriftShopApp', '0002_auto_20200606_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signer', models.CharField(max_length=20, verbose_name='收件人')),
                ('location', models.CharField(max_length=500, verbose_name='位置')),
                ('mobile', models.CharField(max_length=16, verbose_name='手机号')),
                ('add_time', models.DateTimeField(default=datetime.datetime(2020, 6, 6, 9, 4, 29, 186469, tzinfo=utc), verbose_name='添加时间')),
            ],
            options={
                'db_table': 'Address',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.CharField(max_length=1000, verbose_name='签名')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('add_time', models.DateTimeField(default=datetime.datetime(2020, 6, 6, 9, 4, 29, 186469, tzinfo=utc), verbose_name='添加时间')),
            ],
            options={
                'db_table': 'Profile',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 9, 4, 29, 186469, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 9, 4, 29, 186469, tzinfo=utc), verbose_name='加入时间'),
        ),
        migrations.AlterField(
            model_name='order',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 9, 4, 29, 186469, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 9, 4, 29, 186469, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='verifycode',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 9, 4, 29, 186469, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ThriftShopApp.User'),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ThriftShopApp.User'),
        ),
    ]
