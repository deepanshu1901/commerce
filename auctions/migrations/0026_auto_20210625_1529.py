# Generated by Django 3.1.5 on 2021-06-25 09:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_auto_20210625_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bids',
            old_name='listing_name',
            new_name='listing',
        ),
    ]
