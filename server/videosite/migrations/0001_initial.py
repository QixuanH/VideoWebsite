# Generated by Django 4.1.7 on 2023-05-31 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='HistoryRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.IntegerField()),
                ('crate_time', models.DateField()),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('introduction', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('creator_id', models.IntegerField()),
                ('status', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('pwd', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=1)),
                ('history_record', models.ManyToManyField(related_name='record_by_user', to='videosite.historyrecord')),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('introduction', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=1)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos_label', to='videosite.file')),
                ('labels', models.ManyToManyField(to='videosite.label')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='videos_created', to='videosite.user')),
            ],
        ),
        migrations.CreateModel(
            name='Recommend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort', models.IntegerField()),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videosite.video')),
            ],
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videosite.video')),
            ],
        ),
    ]