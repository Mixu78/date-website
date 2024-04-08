# Generated by Django 5.0.3 on 2024-04-08 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staticpages', '0006_remove_staticpage_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='staticpagenav',
            name='url',
            field=models.CharField(blank=True, max_length=200, verbose_name='Url'),
        ),
        migrations.AddField(
            model_name='staticpagenav',
            name='use_category_url',
            field=models.BooleanField(default=False, verbose_name='Använd kategorins URL'),
        ),
    ]
