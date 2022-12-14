# Generated by Django 4.1.3 on 2022-11-22 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_brand_id_alter_category_id_alter_product_id_and_more'),
        ('orders', '0002_rename_address_line_1_order_address_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderproduct',
            old_name='product_price',
            new_name='price',
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='orders.order'),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_product', to='product.product'),
        ),
    ]
