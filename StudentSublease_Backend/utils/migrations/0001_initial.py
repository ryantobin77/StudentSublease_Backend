# Generated by Django 3.2.8 on 2021-10-22 16:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=2, validators=[django.core.validators.RegexValidator('^((A[LKZR])|(C[AOT])|(D[EC])|(FL)|(GA)|(HI)|(I[DLNA])|(K[SY])|(LA)|(M[EDAINSOT])|(N[EVHJMYCD])|(O[HKR])|(PA)|(RI)|(S[CD])|(T[NX])|(UT)|(V[TA])|(W[AVIY]))$')])),
                ('zip', models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^[0-9]{5}$')])),
                ('lat', models.FloatField()),
                ('long', models.FloatField()),
                ('country', models.CharField(max_length=100)),
                ('address_string', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('college_name', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('image', models.ImageField(null=True, upload_to=utils.models.get_file_path)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='utils.address')),
            ],
        ),
        migrations.CreateModel(
            name='CollegeDomain',
            fields=[
                ('domain', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.college')),
            ],
        ),
        migrations.CreateModel(
            name='ClosestCollege',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField(default=0)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='utils.college')),
                ('listing_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utils.address')),
            ],
        ),
    ]
