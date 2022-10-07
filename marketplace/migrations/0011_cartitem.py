# Generated by Django 4.1.1 on 2022-10-02 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0010_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.cart')),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.house')),
            ],
            options={
                'unique_together': {('cart', 'house')},
            },
        ),
    ]
