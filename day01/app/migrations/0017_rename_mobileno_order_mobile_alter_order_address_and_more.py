# Generated by Django 5.1.4 on 2025-01-24 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='mobileno',
            new_name='mobile',
        ),
        migrations.AlterField(
            model_name='order',
            name='address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer',
            field=models.CharField(max_length=50),
        ),
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
