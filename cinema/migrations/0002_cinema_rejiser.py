# Generated by Django 4.2.7 on 2023-12-05 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cinema',
            name='rejiser',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Режисёр'),
        ),
    ]
