# Generated by Django 3.2.6 on 2021-12-22 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0014_goddess_reinforce_chance_eq_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goddess_reinforce_chance',
            name='eq_type',
        ),
        migrations.AddField(
            model_name='goddess_reinforce_mat',
            name='eq_type',
            field=models.CharField(default='armor', max_length=20),
        ),
    ]