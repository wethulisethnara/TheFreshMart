# Generated by Django 5.1.4 on 2025-01-26 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_customer_delete_employee_remove_supplier_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.ManyToManyField(to='app.item'),
        ),
    ]
