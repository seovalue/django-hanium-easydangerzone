# Generated by Django 3.1.2 on 2020-10-18 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteapp', '0002_auto_20201019_0752'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counts',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('visitors', models.IntegerField()),
                ('conversions', models.IntegerField()),
            ],
        ),
    ]
