# Generated by Django 4.2 on 2023-04-22 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_product_description_alter_product_inventory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(default='default_product.png', upload_to='media/'),
        ),
    ]