# Generated by Django 2.1.5 on 2019-02-02 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meme',
            name='flavor',
            field=models.CharField(choices=[('og', 'Original Meme'), ('twit', 'Twit Meme')], default='og', max_length=10, verbose_name='Flavor'),
        ),
    ]
