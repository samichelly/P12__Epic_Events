# Generated by Django 5.0 on 2023-12-13 10:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('company_name', models.CharField(max_length=100)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('last_contact_date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('remaining_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('is_signed', models.BooleanField(default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=255)),
                ('event_date_start', models.DateTimeField()),
                ('event_date_end', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('attendees', models.IntegerField()),
                ('notes', models.TextField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.contract')),
            ],
        ),
    ]