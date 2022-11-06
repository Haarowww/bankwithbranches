# Generated by Django 4.1.2 on 2022-10-27 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('transit_number', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('email', models.EmailField(default='admin@utoronto.ca', max_length=254)),
                ('capacity', models.PositiveIntegerField()),
                ('last_modified', models.DateTimeField()),
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('name', models.CharField(max_length=200)),
                ('swift_code', models.CharField(max_length=200)),
                ('institution_number', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
