# Generated by Django 5.1.4 on 2024-12-31 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='item',
            field=models.ManyToManyField(to='app.item'),
        ),
    ]
