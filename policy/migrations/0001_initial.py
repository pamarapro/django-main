# Generated by Django 4.1.3 on 2022-11-23 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('short_description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/policy')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('visible', models.BooleanField(default=True)),
                ('sort', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Trang chính sách',
                'verbose_name_plural': 'Trang chính sách',
                'ordering': ('-date_added',),
            },
        ),
    ]
