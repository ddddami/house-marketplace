# Generated by Django 4.1.1 on 2022-09-17 05:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='house',
            name='address',
        ),
        migrations.AddField(
            model_name='address',
            name='house',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='marketplace.house'),
            preserve_default=False,
        ),
    ]
