# Generated by Django 4.2.17 on 2024-12-25 16:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_payment_order_id_alter_payment_currency'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apiplan',
            old_name='max_requests_per_month',
            new_name='max_requests_per_day',
        ),
    ]
