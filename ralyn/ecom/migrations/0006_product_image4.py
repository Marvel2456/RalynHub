# Generated by Django 4.2.4 on 2023-09-04 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0005_rename_image_product_image1_product_image2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='item/image'),
        ),
    ]
