# Generated by Django 4.2.17 on 2024-12-29 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0011_alter_clientuser_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
