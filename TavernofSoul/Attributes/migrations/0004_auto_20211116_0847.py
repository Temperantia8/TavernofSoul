# Generated by Django 3.2.9 on 2021-11-16 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Attributes', '0003_alter_attributes_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributes',
            name='id_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='attributes',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
