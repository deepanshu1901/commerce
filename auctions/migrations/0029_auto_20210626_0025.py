# Generated by Django 3.1.5 on 2021-06-25 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0028_auto_20210625_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='listing',
            field=models.ManyToManyField(blank=True, null=True, related_name='watchlist_item', to='auctions.Listing'),
        ),
    ]
