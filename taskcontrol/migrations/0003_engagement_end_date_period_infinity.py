# Generated by Django 5.0.3 on 2024-05-27 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskcontrol', '0002_alter_registertax_company_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='engagement',
            name='end_date_period_infinity',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
