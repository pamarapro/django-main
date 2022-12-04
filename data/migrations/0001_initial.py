# Generated by Django 4.1.3 on 2022-11-23 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity', models.CharField(blank=True, help_text='Nhập thông tin tên website tối đa 60 ký tự', max_length=200, null=True)),
                ('content', models.TextField(blank=True, help_text='Nhập thông tin tên website tối đa 155 ký tự', null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='uploads/site')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='uploads/site')),
                ('services', models.TextField(blank=True, null=True)),
                ('header_script', models.TextField(blank=True, null=True)),
                ('body_script', models.TextField(blank=True, null=True)),
                ('css_script', models.TextField(blank=True, null=True)),
                ('website', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('facebook', models.CharField(blank=True, max_length=100, null=True)),
                ('zalo', models.CharField(blank=True, max_length=100, null=True)),
                ('zalo_oaid', models.CharField(blank=True, max_length=100, null=True)),
                ('google', models.CharField(blank=True, max_length=100, null=True)),
                ('instagram', models.CharField(blank=True, max_length=100, null=True)),
                ('map_iframe', models.TextField(blank=True, null=True)),
                ('header_text', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Thông tin công ty',
                'verbose_name_plural': 'Thông tin công ty',
            },
        ),
    ]