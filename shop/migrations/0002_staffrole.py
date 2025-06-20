# Generated by Django 5.0.12 on 2025-02-27 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'staff role',
                'verbose_name_plural': 'staff roles',
                'ordering': ['name'],
                'indexes': [models.Index(fields=['name'], name='shop_staffr_name_edb128_idx')],
            },
        ),
    ]
