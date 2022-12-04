# Generated by Django 4.1.3 on 2022-11-25 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_product_price_orderproduct_price_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Đơn hàng', 'verbose_name_plural': 'Đơn hàng'},
        ),
        migrations.AlterModelOptions(
            name='orderproduct',
            options={'verbose_name': 'Sản phẩm đặt hàng', 'verbose_name_plural': 'Sản phẩm đặt hàng'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Phương thức thanh toán', 'verbose_name_plural': 'Phương thức thanh toán'},
        ),
        migrations.AlterField(
            model_name='order',
            name='is_ordered',
            field=models.BooleanField(default=True),
        ),
    ]