# Generated by Django 2.0.2 on 2018-02-25 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chap3_2_1', '0024_auto_20180225_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramuser',
            name='following',
            field=models.ManyToManyField(related_name='followers', to='chap3_2_1.InstagramUser'),
        ),
    ]
