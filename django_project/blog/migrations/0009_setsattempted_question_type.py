# Generated by Django 3.0.5 on 2020-04-12 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_choice_question_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='setsattempted',
            name='question_type',
            field=models.CharField(default=0, max_length=5),
            preserve_default=False,
        ),
    ]