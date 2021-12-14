# Generated by Django 3.2.6 on 2021-11-02 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buffs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.CharField(db_index=True, max_length=30)),
                ('id_name', models.CharField(max_length=30)),
                ('icon', models.CharField(blank=True, max_length=30, null=True)),
                ('name', models.CharField(max_length=30)),
                ('descriptions', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('applytime', models.IntegerField(blank=True, null=True)),
                ('group1', models.CharField(blank=True, max_length=30, null=True)),
                ('group2', models.CharField(blank=True, max_length=30, null=True)),
                ('group3', models.CharField(blank=True, max_length=30, null=True)),
                ('groupindex', models.CharField(blank=True, max_length=30, null=True)),
                ('overbuff', models.IntegerField(default=0)),
                ('userremove', models.BooleanField(default=False)),
            ],
        ),
    ]