# Generated by Django 3.2.6 on 2022-01-11 08:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0021_auto_20220106_1411'),
        ('Jobs', '0002_auto_20211015_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobs',
            name='vaivora',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Items.equipments'),
        ),
    ]
