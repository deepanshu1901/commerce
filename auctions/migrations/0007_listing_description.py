# Generated by Django 3.1.5 on 2021-06-23 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210623_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='description',
            field=models.CharField(default='', max_length=600),
        ),
    ]