# Generated by Django 5.0.4 on 2024-04-08 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_users_stockbuy_users_stocksold'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='password',
            field=models.CharField(default=0, max_length=128),
        ),
    ]
