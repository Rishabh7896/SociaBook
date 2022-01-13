# Generated by Django 3.2.3 on 2021-06-02 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20210603_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='picturemessage',
            field=models.ImageField(null=True, upload_to='message'),
        ),
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=models.ImageField(upload_to='post'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profilepic',
            field=models.ImageField(default='default.jpg', upload_to='profilepic'),
        ),
    ]