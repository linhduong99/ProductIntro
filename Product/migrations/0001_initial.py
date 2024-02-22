# Generated by Django 4.2.10 on 2024-02-22 02:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('image', models.ImageField(upload_to='upload_images/categories')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField(default='')),
                ('categories', models.ManyToManyField(to='Product.category')),
            ],
        ),
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('image', models.ImageField(upload_to='upload_images/promotions')),
                ('ordinal', models.IntegerField(default=0, verbose_name='ordinal')),
                ('start_time', models.DateTimeField(verbose_name='start_time')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='end_time')),
                ('status', models.CharField(choices=[('completed', 'Completed'), ('publish', 'Publish'), ('draft', 'Draft')], default='draft', max_length=16, verbose_name='status')),
            ],
            options={
                'verbose_name': 'Promotion',
                'verbose_name_plural': 'Promotions',
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='upload_images/products')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.product')),
            ],
        ),
    ]
