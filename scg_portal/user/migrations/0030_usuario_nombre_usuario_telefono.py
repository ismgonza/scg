# Generated by Django 5.0 on 2024-02-28 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0029_remove_usuario_nombre_remove_usuario_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='nombre',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
