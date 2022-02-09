# Generated by Django 3.2.6 on 2022-02-03 03:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Market', '0002_auto_20220203_1010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goods',
            name='created',
        ),
        migrations.RemoveField(
            model_name='goods',
            name='updated',
        ),
        migrations.AddField(
            model_name='crawl_info',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]