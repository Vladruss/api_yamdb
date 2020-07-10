# Generated by Django 3.0.5 on 2020-07-10 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20200709_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='api.Category'),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(related_name='genres', to='api.Genre'),
        ),
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.IntegerField(),
        ),
    ]
