# Generated by Django 4.1.3 on 2022-11-25 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='policy',
            options={'ordering': ('-date_added',), 'verbose_name': 'Trang nội dung', 'verbose_name_plural': 'Trang nội dung'},
        ),
    ]
