# Generated by Django 4.1.3 on 2022-11-22 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'verbose_name': 'Mã khuyến mãi', 'verbose_name_plural': 'Mã khuyến mãi'},
        ),
        migrations.AlterModelOptions(
            name='promotion',
            options={'verbose_name': 'Banner chương trình', 'verbose_name_plural': 'Banner chương trình'},
        ),
        migrations.AlterField(
            model_name='promotion',
            name='banner_size',
            field=models.CharField(blank=True, choices=[('nhỏ', 'Size nhỏ: 300x400'), ('thường', 'Size thường: 600x900'), ('rộng', 'Size rộng: 1200x200')], default='nhỏ', max_length=9, null=True),
        ),
    ]
