# Generated by Django 5.0 on 2024-02-15 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vocabulaire', '0012_alter_update_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homework',
            name='created',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='update',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
