# Generated by Django 5.0 on 2023-12-20 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_alter_usuario_correo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='correo',
            field=models.CharField(max_length=100),
        ),
    ]
