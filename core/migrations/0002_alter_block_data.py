# Generated by Django 4.0.4 on 2022-06-10 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='data',
            field=models.TextField(),
        ),
    ]
