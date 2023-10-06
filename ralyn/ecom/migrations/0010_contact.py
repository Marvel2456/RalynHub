# Generated by Django 4.2.4 on 2023-09-26 22:23

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0009_remove_paymenthistory_ref_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=225, null=True)),
                ('email', models.CharField(blank=True, max_length=225, null=True)),
                ('subject', models.CharField(blank=True, max_length=225, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]