# Generated by Django 4.1.2 on 2022-11-14 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0002_student_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.CharField(default='test@test.mail.ru', max_length=120, verbose_name='Электронная почта'),
        ),
    ]
