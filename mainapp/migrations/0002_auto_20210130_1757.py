# Generated by Django 3.1.3 on 2021-01-30 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='mainapp.CartProduct'),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='object_id',
            field=models.PositiveIntegerField(),
        ),
    ]