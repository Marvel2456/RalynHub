# Generated by Django 4.2.4 on 2023-09-05 15:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=225, null=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('Ordered_at', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(blank=True, default=False, null=True)),
                ('transaction_id', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(blank=True, max_length=225, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='remark/image')),
                ('client_remark', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ShippingDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=225, null=True)),
                ('city', models.CharField(blank=True, max_length=225, null=True)),
                ('state', models.CharField(blank=True, max_length=225, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=225, null=True)),
                ('phone', models.CharField(blank=True, max_length=225, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom.order')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='item/image')),
                ('image1', models.ImageField(blank=True, null=True, upload_to='item/image')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='item/image')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='item/image')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='item/image')),
                ('description', models.TextField(blank=True, null=True)),
                ('store_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('is_popular', models.BooleanField(blank=True, default=False, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('quantity', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom.order')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ecom.product')),
            ],
        ),
    ]
