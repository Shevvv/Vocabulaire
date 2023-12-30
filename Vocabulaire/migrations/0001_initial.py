# Generated by Django 5.0 on 2023-12-28 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Russian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lexeme', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Dutch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lexeme', models.CharField(max_length=200)),
                ('translations', models.ManyToManyField(to='Vocabulaire.russian')),
            ],
        ),
    ]