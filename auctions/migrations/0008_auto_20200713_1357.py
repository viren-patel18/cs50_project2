# Generated by Django 3.0.8 on 2020-07-13 17:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_bid_category_comment_listing_watchlist'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='listings',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='listing',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='listings',
        ),
        migrations.RemoveField(
            model_name='watchlist',
            name='user',
        ),
        migrations.DeleteModel(
            name='Bid',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Listing',
        ),
        migrations.DeleteModel(
            name='Watchlist',
        ),
    ]
