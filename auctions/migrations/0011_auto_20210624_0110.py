# Generated by Django 3.1.5 on 2021-06-23 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20210624_0046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listing',
            field=models.ManyToManyField(blank=True, related_name='watchlist_item', to='auctions.Listing'),
        ),
    ]
