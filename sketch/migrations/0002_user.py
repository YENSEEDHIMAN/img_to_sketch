# Generated by Django 5.1.7 on 2025-03-25 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sketch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
