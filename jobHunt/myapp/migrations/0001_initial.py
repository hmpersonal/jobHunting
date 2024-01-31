# Generated by Django 5.0.1 on 2024-01-29 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AiAnalysisLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('autoIncId', models.IntegerField()),
                ('imagePath', models.CharField(max_length=255)),
                ('success', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('cls', models.IntegerField()),
                ('confidence', models.DecimalField(decimal_places=4, max_digits=5)),
                ('requestTimestamp', models.IntegerField()),
                ('responseTimeStamp', models.IntegerField()),
            ],
        ),
    ]