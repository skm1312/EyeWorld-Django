# Generated by Django 3.0.8 on 2021-03-13 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='type_user',
            field=models.CharField(choices=[('normal', 'normal'), ('opto', 'opto')], default='normal', max_length=20),
        ),
    ]
