# Generated by Django 4.2.1 on 2023-05-19 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_usuarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Suscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombrecompleto', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('correo', models.CharField(max_length=100)),
                ('numerotelefono', models.IntegerField()),
                ('contraseña', models.CharField(max_length=100)),
                ('confirmarcontraseña', models.CharField(max_length=100)),
                ('numerotarjeta', models.IntegerField()),
                ('fechavencimiento', models.CharField(max_length=100)),
                ('cvv', models.IntegerField()),
            ],
        ),
        migrations.DeleteModel(
            name='Usuarios',
        ),
    ]
