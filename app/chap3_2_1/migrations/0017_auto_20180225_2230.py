# Generated by Django 2.0.2 on 2018-02-25 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chap3_2_1', '0016_auto_20180225_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramuser',
            name='following',
            field=models.ManyToManyField(to='chap3_2_1.InstagramUser'),
        ),
    ]
