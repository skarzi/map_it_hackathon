# Generated by Django 2.0.9 on 2018-11-18 02:43

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TransportEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('latitude', models.FloatField()),
                ('longtitude', models.FloatField()),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='TransportType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
                ('icon', models.ImageField(upload_to='icons')),
            ],
        ),
        migrations.AddField(
            model_name='transportevent',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to='transports.TransportType'),
        ),
    ]
