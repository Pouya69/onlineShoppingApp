# Generated by Django 4.0.1 on 2022-01-05 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('review_score', models.DecimalField(decimal_places=1, max_digits=3)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='pics/')),
                ('comments', models.ManyToManyField(blank=True, default=None, related_name='comments_of_users', to='shopping.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField()),
                ('description', models.TextField(default='', max_length=2000)),
                ('shipping_type', models.CharField(choices=[('standard', 'Standard'), ('premium', 'Premium')], max_length=9)),
                ('final_price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('ordered_by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_ordered', to='shopping.userapp')),
                ('products', models.ManyToManyField(blank=True, default=None, related_name='products_in_cart', to='shopping.Product')),
            ],
        ),
    ]
