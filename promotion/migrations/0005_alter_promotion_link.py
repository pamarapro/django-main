# Generated by Django 4.1.3 on 2022-11-30 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promotion', '0004_promotion_link_alter_promotion_banner_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
