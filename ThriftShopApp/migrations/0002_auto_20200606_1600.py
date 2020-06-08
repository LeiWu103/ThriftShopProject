# Generated by Django 2.1.13 on 2020-06-06 08:00

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ThriftShopApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_sn', models.IntegerField(unique=True, verbose_name='订单号')),
                ('status', models.CharField(max_length=10, verbose_name='订单状态')),
                ('quantity', models.IntegerField(verbose_name='订购数量')),
                ('amount', models.FloatField(verbose_name='订单金额')),
                ('message', models.CharField(max_length=200, verbose_name='订单留言')),
                ('add_time', models.DateTimeField(default=datetime.datetime(2020, 6, 6, 8, 0, 36, 616005, tzinfo=utc), verbose_name='添加时间')),
            ],
            options={
                'db_table': 'Order',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 8, 0, 36, 616005, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='goods',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 8, 0, 36, 616005, tzinfo=utc), verbose_name='加入时间'),
        ),
        migrations.AlterField(
            model_name='user',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 8, 0, 36, 616005, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AlterField(
            model_name='verifycode',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 6, 6, 8, 0, 36, 616005, tzinfo=utc), verbose_name='添加时间'),
        ),
        migrations.AddField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='ThriftShopApp.User'),
        ),
        migrations.AddField(
            model_name='order',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ThriftShopApp.Goods'),
        ),
        migrations.AddField(
            model_name='order',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller', to='ThriftShopApp.User'),
        ),
    ]
