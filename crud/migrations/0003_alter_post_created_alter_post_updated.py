# Generated by Django 5.0.6 on 2024-06-27 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud', '0002_remove_post_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]