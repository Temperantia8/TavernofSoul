# Generated by Django 3.2.7 on 2021-10-15 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0002_auto_20211015_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment_set',
            name='bonus2',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='equipment_set',
            name='bonus3',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='equipment_set',
            name='bonus4',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='equipment_set',
            name='bonus5',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='equipment_set',
            name='bonus6',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='equipment_set',
            name='bonus7',
            field=models.CharField(blank=True, default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='equipment_set',
            name='name',
            field=models.CharField(blank=True, default=None, max_length=50),
        ),
    ]
