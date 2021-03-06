# Generated by Django 3.1.11 on 2021-05-15 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dsrs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dsr',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dsrs', to='dsrs.currency'),
        ),
        migrations.AlterField(
            model_name='dsr',
            name='territory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dsrs', to='dsrs.territory'),
        ),
        migrations.AlterField(
            model_name='territory',
            name='local_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='territories', to='dsrs.currency'),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dsp_id', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=64)),
                ('artists', models.CharField(max_length=64)),
                ('isrc', models.CharField(max_length=16)),
                ('usages', models.IntegerField()),
                ('revenue', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dsrs', models.ManyToManyField(related_name='resources', to='dsrs.DSR')),
            ],
            options={
                'db_table': 'resource',
            },
        ),
    ]
