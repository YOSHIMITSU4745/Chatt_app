# Generated by Django 5.0.6 on 2024-07-14 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_room_participants'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='private',
            field=models.CharField(default='yes', max_length=100),
            preserve_default=False,
        ),
    ]
