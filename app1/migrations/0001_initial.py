# Generated by Django 5.0.4 on 2024-04-07 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('username', models.CharField(max_length=52, primary_key=True, serialize=False)),
                ('firstname', models.CharField(max_length=52)),
                ('lastname', models.CharField(max_length=52)),
                ('email', models.EmailField(max_length=254)),
                ('datajoined', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]