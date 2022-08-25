# Generated by Django 3.1.13 on 2022-08-21 12:39

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ctf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Titel')),
                ('content', ckeditor.fields.RichTextField(blank=True, verbose_name='Innehåll')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('slug', models.SlugField(unique=True, verbose_name='Slug')),
                ('published', models.BooleanField(default=True, verbose_name='Publicera')),
            ],
            options={
                'verbose_name': 'ctf',
                'verbose_name_plural': 'ctf',
            },
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('flag', models.CharField(max_length=200)),
                ('clues', ckeditor.fields.RichTextField(blank=True, verbose_name='Clue')),
                ('ctf', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctf.ctf')),
                ('solver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Flag',
                'verbose_name_plural': 'Flags',
            },
        ),
    ]
