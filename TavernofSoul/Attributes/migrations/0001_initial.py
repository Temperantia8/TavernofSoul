# Generated by Django 3.2.7 on 2021-10-08 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Skills', '0001_initial'),
        ('Jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attributes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ids', models.CharField(db_index=True, max_length=30)),
                ('id_name', models.CharField(max_length=30)),
                ('descriptions', models.TextField()),
                ('descriptions_required', models.TextField(blank=True, null=True)),
                ('icon', models.CharField(max_length=50)),
                ('is_toggleable', models.BooleanField()),
                ('max_lv', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('job', models.ManyToManyField(to='Jobs.Jobs')),
                ('skill', models.ManyToManyField(to='Skills.Skills')),
            ],
        ),
    ]
