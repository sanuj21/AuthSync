# Generated by Django 4.2.17 on 2024-12-24 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientuser',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='clientuser',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('USER ', 'User')], default='USER ', max_length=10),
        ),
        migrations.AlterField(
            model_name='clientuser',
            name='email_verification_token',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='clientuser',
            name='reset_token',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True),
        ),
    ]
