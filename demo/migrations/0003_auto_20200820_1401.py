# Generated by Django 3.1 on 2020-08-20 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_auto_20200817_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorites',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demo.product'),
        ),
    ]
