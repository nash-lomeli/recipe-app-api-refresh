# Generated by Django 4.2.9 on 2024-02-04 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('completed_instructions', '0001_initial'),
        ('recipes', '0003_instructioningredient'),
    ]

    operations = [
        migrations.AddField(
            model_name='instruction',
            name='completed',
            field=models.ManyToManyField(blank=True, related_name='completed_by', through='completed_instructions.CompletedInstruction', to='profiles.profile'),
        ),
    ]
