# Generated by Django 5.0 on 2024-04-02 20:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0057_alter_usuario_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id_comment', models.BigAutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField(max_length=100)),
                ('fecha', models.DateTimeField(auto_now=True)),
                ('loe', models.FloatField(blank=True, max_length=100, null=True)),
                ('tarea_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tareas_comments', to='user.tarea')),
            ],
        ),
    ]
