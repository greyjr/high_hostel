# Generated by Django 2.0 on 2020-07-20 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('work_app', '0003_auto_20200707_0024'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=128)),
                ('register_date', models.DateTimeField()),
                ('instance', models.CharField(max_length=32)),
                ('action', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='order_client',
            field=models.ForeignKey(default=42, on_delete=django.db.models.deletion.CASCADE, to='work_app.Client'),
        ),
    ]
