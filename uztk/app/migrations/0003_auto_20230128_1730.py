# Generated by Django 3.2.15 on 2023-01-28 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20230128_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='tourniquetlock',
            name='lock_type',
            field=models.IntegerField(choices=[(1, 'Турникет'), (2, 'Замок')], db_index=True, default=1, verbose_name='Тип'),
        ),
        migrations.AlterField(
            model_name='camera',
            name='camtype',
            field=models.IntegerField(choices=[(1, 'Следящая'), (2, 'Распознающая'), (3, 'Управляющая')], default=1, verbose_name='Тип камеры (1-3)'),
        ),
    ]
