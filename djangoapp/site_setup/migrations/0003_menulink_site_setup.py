# Generated by Django 4.2.9 on 2024-01-14 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0002_sitesetup'),
    ]

    operations = [
        migrations.AddField(
            model_name='menulink',
            name='site_setup',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='site_setup.sitesetup'),
        ),
    ]
