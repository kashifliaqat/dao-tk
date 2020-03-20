# Generated by Django 3.0.3 on 2020-03-14 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardDataRTO',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp')),
                ('actual', models.FloatField(default=None, verbose_name='Actual [MWe]')),
                ('optimal', models.FloatField(default=None, verbose_name='Optimal [MWe]')),
                ('scheduled', models.FloatField(default=None, verbose_name='Scheduled [MWe]')),
                ('field_operation_generated', models.FloatField(default=None, verbose_name='Field Operation Generated [MWt]')),
                ('field_operation_available', models.FloatField(default=None, verbose_name='Field Operation Available [MWt]')),
            ],
        ),
        migrations.CreateModel(
            name='ForecastsMarketData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp')),
                ('market_forecast', models.FloatField(default=None, verbose_name='Market Forcast [-]')),
                ('ci_plus', models.FloatField(default=None, verbose_name='CI+ [%]')),
                ('ci_minus', models.FloatField(default=None, verbose_name='CI- [%]')),
            ],
        ),
        migrations.CreateModel(
            name='ForecastsSolarData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='Timestamp')),
                ('clear_sky', models.FloatField(default=None, verbose_name='Clear Sky [W/m2]')),
                ('nam', models.FloatField(default=None, verbose_name='NAM [W/m2]')),
                ('nam_plus', models.FloatField(default=None, verbose_name='NAM+ [%]')),
                ('nam_minus', models.FloatField(default=None, verbose_name='NAM- [%]')),
                ('rap', models.FloatField(default=None, verbose_name='RAP [W/m2]')),
                ('rap_plus', models.FloatField(default=None, verbose_name='RAP+ [%]')),
                ('rap_minus', models.FloatField(default=None, verbose_name='RAP- [%]')),
                ('hrrr', models.FloatField(default=None, verbose_name='HRRR [W/m2]')),
                ('hrrr_plus', models.FloatField(default=None, verbose_name='HRRR+ [%]')),
                ('hrrr_minus', models.FloatField(default=None, verbose_name='HRRR- [%]')),
                ('gfs', models.FloatField(default=None, verbose_name='GFS [W/m2]')),
                ('gfs_plus', models.FloatField(default=None, verbose_name='GFS+ [%]')),
                ('gfs_minus', models.FloatField(default=None, verbose_name='GFS- [%]')),
                ('ndfd', models.FloatField(default=None, verbose_name='NDFD [W/m2]')),
                ('ndfd_plus', models.FloatField(default=None, verbose_name='NDFD+ [%]')),
                ('ndfd_minus', models.FloatField(default=None, verbose_name='NDFD- [%]')),
            ],
        ),
    ]