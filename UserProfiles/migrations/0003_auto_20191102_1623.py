# Generated by Django 2.2.5 on 2019-11-02 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfiles', '0002_auto_20191026_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='default1.jpg', null=True, upload_to='profile_pics/'),
        ),
    ]
