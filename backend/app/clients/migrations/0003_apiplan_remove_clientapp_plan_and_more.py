# Generated by Django 4.2.17 on 2024-12-25 11:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiPlan',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('max_requests_per_month', models.IntegerField()),
                ('max_users', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='clientapp',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='client_app',
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('client_app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='clients.clientapp')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='clients.apiplan')),
            ],
        ),
        migrations.AddField(
            model_name='payment',
            name='subscription',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='clients.subscription'),
            preserve_default=False,
        ),
    ]
