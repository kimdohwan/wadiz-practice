# Generated by Django 2.0.7 on 2018-07-31 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_description', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=20)),
                ('background_image_url', models.CharField(max_length=200)),
                ('company', models.CharField(max_length=50)),
                ('number_of_days_remaining', models.CharField(max_length=50)),
                ('rate_of_achivement', models.CharField(max_length=50)),
                ('cur_amount_of_funding', models.CharField(max_length=50)),
                ('description_html', models.TextField()),
                ('number_of_supporters', models.CharField(max_length=50)),
                ('goal_amount', models.CharField(max_length=50)),
            ],
        ),
    ]
