# Generated by Django 5.1 on 2024-08-11 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0007_functionaryrole_functionary'),
    ]

    operations = [
        migrations.AddField(
            model_name='alumnisignup',
            name='operation',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
