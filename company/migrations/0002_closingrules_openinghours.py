# Generated by Django 2.1.7 on 2019-05-01 12:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClosingRules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField(verbose_name='Start')),
                ('end', models.DateTimeField(verbose_name='End')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='Reason')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Closing Rule',
                'verbose_name_plural': 'Closing Rules',
                'ordering': ['start'],
            },
        ),
        migrations.CreateModel(
            name='OpeningHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weekday', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')], verbose_name='Weekday')),
                ('from_hour', models.TimeField(verbose_name='Opening')),
                ('to_hour', models.TimeField(verbose_name='Closing')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Opening Hours',
                'verbose_name_plural': 'Opening Hours',
                'ordering': ['company', 'weekday', 'from_hour'],
            },
        ),
    ]
