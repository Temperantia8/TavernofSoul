# Generated by Django 3.2.6 on 2021-12-24 03:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Items', '0016_alter_equipments_anvil_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipments',
            name='anvil_atk',
        ),
        migrations.RemoveField(
            model_name='equipments',
            name='anvil_def',
        ),
        migrations.RemoveField(
            model_name='equipments',
            name='anvil_price',
        ),
        migrations.CreateModel(
            name='Eq_TC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField()),
                ('tc', models.IntegerField()),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Items.equipments')),
            ],
        ),
        migrations.CreateModel(
            name='Eq_Reinf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anvil', models.IntegerField()),
                ('price', models.IntegerField()),
                ('addatk', models.IntegerField()),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Items.equipments')),
            ],
        ),
    ]
