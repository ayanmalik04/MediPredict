# Generated by Django 5.0.2 on 2024-06-28 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginsys', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ContactMessage',
            new_name='ContactMessages',
        ),
        migrations.AlterField(
            model_name='pointadata11',
            name='doctor',
            field=models.CharField(choices=[('Cardiologist', 'Cardiologist'), ('Nephrologist', 'Nephrologist'), ('Oncologist', 'Oncologist'), ('Disease Specialist', 'Infectious Disease Specialist'), ('General Surgeon', 'General Surgeon'), ('Medicine Specialist', 'Internal Medicine Specialist')], max_length=20),
        ),
        migrations.AlterField(
            model_name='pointadata11',
            name='name',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterModelTable(
            name='contactmessages',
            table='contactdata',
        ),
    ]
