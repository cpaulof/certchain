# Generated by Django 4.0.4 on 2022-06-10 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_block_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='previous_hash',
            field=models.CharField(max_length=512, null=True),
        ),
        migrations.AlterField(
            model_name='block',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
