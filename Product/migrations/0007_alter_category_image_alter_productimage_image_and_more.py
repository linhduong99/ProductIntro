# Generated by Django 4.2.10 on 2024-02-22 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0006_productimage_ordinal'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(upload_to='media/categories'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='media/products'),
        ),
        migrations.AlterField(
            model_name='promotions',
            name='image',
            field=models.ImageField(upload_to='media/promotions'),
        ),
    ]
