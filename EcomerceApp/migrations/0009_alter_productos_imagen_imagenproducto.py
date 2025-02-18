# Generated by Django 5.1.3 on 2024-12-09 22:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcomerceApp', '0008_remove_categoria_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='productos/', verbose_name='Imagen_Principal'),
        ),
        migrations.CreateModel(
            name='ImagenProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='productos/otras_imagenes/', verbose_name='Imagenes Adicionales')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Imagenes_Adicionales', to='EcomerceApp.productos', verbose_name='Producto')),
            ],
        ),
    ]
