# Generated by Django 3.1.5 on 2021-06-25 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_comment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(default=''),
        ),
    ]
