# Generated by Django 5.0 on 2024-06-26 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0065_alter_tarea_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='descripcion',
            field=models.TextField(blank=True, max_length=10000, null=True),
        ),
    ]
