# Generated by Django 3.0.8 on 2021-08-27 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('token_validation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
    ]