# Generated by Django 5.1.7 on 2025-03-26 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ambulance_app', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Clinic',
        ),
        migrations.RenameField(
            model_name='hospital',
            old_name='occupied_beds',
            new_name='remaining_beds',
        ),
        migrations.RemoveField(
            model_name='hospital',
            name='capacity',
        ),
        migrations.AlterField(
            model_name='ambulance',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='hospital',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trafficsignal',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='trafficsignal',
            name='status',
            field=models.CharField(choices=[('GREEN', 'Green'), ('RED', 'Red')], max_length=10),
        ),
    ]
