# Generated by Django 4.2.3 on 2023-09-16 01:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='media',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.PROTECT, related_name='all_appearances', to='tracker.media'),
        ),
    ]