# Generated by Django 4.1.3 on 2022-11-22 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'verbose_name': 'Tác giả', 'verbose_name_plural': 'Tác giả'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Chuyên mục', 'verbose_name_plural': 'Chuyên mục'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-posted_date',), 'verbose_name': 'Bài viết', 'verbose_name_plural': 'Bài viết'},
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(help_text='Không nhập quá 70 ký tự', max_length=100),
        ),
    ]