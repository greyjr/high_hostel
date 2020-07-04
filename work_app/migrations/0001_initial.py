# Generated by Django 2.0 on 2020-06-21 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('patronymic', models.CharField(max_length=64)),
                ('passport', models.CharField(max_length=128)),
                ('another_document', models.CharField(max_length=128, null=True)),
                ('phone', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254)),
                ('comment', models.CharField(default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('date_stop', models.DateField()),
                ('order_bed', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='work_app.Bed')),
                ('order_client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work_app.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('number', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='bed',
            name='bed_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work_app.Room'),
        ),
    ]