# Generated by Django 2.1.7 on 2019-06-05 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('location', '0001_initial'),
        ('company', '0001_initial'),
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('salary', models.CharField(blank=True, max_length=128)),
                ('description', models.TextField(help_text='qualification, responsibilities,  requirements,  benefits, Experience')),
                ('application_info', models.TextField(help_text="What's the best way to apply for this job?")),
                ('work_hours', models.CharField(blank=True, max_length=80)),
                ('url', models.CharField(blank=True, max_length=1024)),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('opening', models.IntegerField(blank=True, default=1, null=True)),
                ('remote', models.BooleanField(default=False, help_text='Select if this job allows 100% remote working')),
                ('publish', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='job', to='category.Category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='company.Company')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='job', to='location.Location')),
            ],
        ),
        migrations.CreateModel(
            name='TaggedJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_object', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='job.Job')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_taggedjob_items', to='taggit.Tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='job',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='job.TaggedJob', to='taggit.Tag', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='job',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='job', to=settings.AUTH_USER_MODEL),
        ),
    ]
