# Generated by Django 4.2.1 on 2023-06-10 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SpamDetect', '0003_alter_contact_phone_number_alter_spam_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
