# Generated by Django 3.0.8 on 2020-07-13 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_delete_listing'),
    ]

    operations = [
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
            name='Watchlist',
        ),
    ]