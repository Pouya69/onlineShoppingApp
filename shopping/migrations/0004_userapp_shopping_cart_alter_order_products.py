# Generated by Django 4.0.1 on 2022-01-05 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_product_category_userapp_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='userapp',
            name='shopping_cart',
            field=models.ManyToManyField(blank=True, default=None, related_name='products_in_cart', to='shopping.Product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(blank=True, default=None, related_name='products_bought', to='shopping.Product'),
        ),
    ]
