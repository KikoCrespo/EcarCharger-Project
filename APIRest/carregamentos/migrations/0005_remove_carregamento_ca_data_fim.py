# Generated by Django 4.2.20 on 2025-05-27 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("carregamentos", "0004_alter_carregamento_ca_data_fim_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="carregamento",
            name="ca_data_fim",
        ),
    ]
