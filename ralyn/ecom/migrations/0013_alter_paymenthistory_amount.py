# Generated by Django 4.2.4 on 2023-09-29 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0012_paymenthistory_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymenthistory',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
