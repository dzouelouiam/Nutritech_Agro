# Generated by Django 3.2.25 on 2024-10-26 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20241026_1357'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default='default_user', max_length=150, unique=True),
        ),
    ]
