# Generated by Django 3.2.3 on 2021-06-02 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_auto_20210603_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profilepic',
            field=models.ImageField(default='default.jpg', upload_to='profilepic'),
        ),
    ]
