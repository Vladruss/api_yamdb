# Generated by Django 3.0.5 on 2020-07-07 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200701_1445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('slug', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('slug', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=50)),
                ('year', models.DateField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='category', to='api.Category')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='genre', to='api.Genre')),
            ],
        ),
    ]
