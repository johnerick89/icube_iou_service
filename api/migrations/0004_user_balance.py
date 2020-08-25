# Generated by Django 3.1 on 2020-08-25 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200825_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=4, default=0.0, max_digits=25),
            preserve_default=False,
        ),
    ]
