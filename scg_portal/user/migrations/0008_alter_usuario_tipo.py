# Generated by Django 5.0 on 2023-12-22 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_usuario_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(choices=[('Admin', 'Admin'), ('Cliente', 'Cliente')], max_length=100),
        ),
    ]
