# Generated by Django 4.1.1 on 2022-09-21 20:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0006_houseimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='houseimage',
            name='house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='marketplace.house'),
        ),
    ]
