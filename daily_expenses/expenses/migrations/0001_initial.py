# Generated by Django 5.0.7 on 2024-07-29 11:01

import django.db.models.deletion
import jsonfield.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('members', jsonfield.fields.JSONField()),
                ('split_method', models.CharField(choices=[('equal', 'Equal'), ('exact', 'Exact'), ('percentage', 'Percentage')], max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('mobile_number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SplitDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.EmailField(max_length=254)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('expense_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.expense')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.user')),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.user'),
        ),
    ]