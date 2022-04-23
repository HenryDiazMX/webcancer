# Generated by Django 4.0.2 on 2022-04-18 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cancerinfantil', '0007_republicav2'),
    ]

    operations = [
        migrations.CreateModel(
            name='Casostotalrepublica',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('ent_regis', models.TextField(blank=True, db_column='ENT_REGIS', null=True)),
                ('mun_regis', models.TextField(blank=True, db_column='MUN_REGIS', null=True)),
                ('ent_resid', models.TextField(blank=True, db_column='ENT_RESID', null=True)),
                ('mun_resid', models.TextField(blank=True, db_column='MUN_RESID', null=True)),
                ('tloc_resid', models.TextField(blank=True, db_column='TLOC_RESID', null=True)),
                ('loc_resid', models.TextField(blank=True, db_column='LOC_RESID', null=True)),
                ('ent_ocurr', models.TextField(blank=True, db_column='ENT_OCURR', null=True)),
                ('mun_ocurr', models.TextField(blank=True, db_column='MUN_OCURR', null=True)),
                ('tloc_ocurr', models.TextField(blank=True, db_column='TLOC_OCURR', null=True)),
                ('loc_ocurr', models.TextField(blank=True, db_column='LOC_OCURR', null=True)),
                ('causa_def', models.TextField(blank=True, db_column='CAUSA_DEF', null=True)),
                ('lista_mex', models.TextField(blank=True, db_column='LISTA_MEX', null=True)),
                ('sexo', models.TextField(blank=True, db_column='SEXO', null=True)),
                ('edad', models.TextField(blank=True, db_column='EDAD', null=True)),
                ('dia_ocurr', models.TextField(blank=True, db_column='DIA_OCURR', null=True)),
                ('mes_ocurr', models.TextField(blank=True, db_column='MES_OCURR', null=True)),
                ('anio_ocur', models.TextField(blank=True, db_column='ANIO_OCUR', null=True)),
                ('dia_regis', models.TextField(blank=True, db_column='DIA_REGIS', null=True)),
                ('mes_regis', models.TextField(blank=True, db_column='MES_REGIS', null=True)),
                ('anio_regis', models.BigIntegerField(blank=True, db_column='ANIO_REGIS', null=True)),
                ('dia_nacim', models.TextField(blank=True, db_column='DIA_NACIM', null=True)),
                ('mes_nacim', models.TextField(blank=True, db_column='MES_NACIM', null=True)),
                ('anio_nacim', models.TextField(blank=True, db_column='ANIO_NACIM', null=True)),
                ('ocupacion', models.TextField(blank=True, db_column='OCUPACION', null=True)),
                ('escolarida', models.TextField(blank=True, db_column='ESCOLARIDA', null=True)),
                ('edo_civil', models.TextField(blank=True, db_column='EDO_CIVIL', null=True)),
                ('necropsia', models.TextField(blank=True, db_column='NECROPSIA', null=True)),
                ('asist_medi', models.TextField(blank=True, db_column='ASIST_MEDI', null=True)),
                ('sitio_ocur', models.TextField(blank=True, db_column='SITIO_OCUR', null=True)),
                ('cond_cert', models.TextField(blank=True, db_column='COND_CERT', null=True)),
                ('nacionalid', models.TextField(blank=True, db_column='NACIONALID', null=True)),
                ('derechohab', models.TextField(blank=True, db_column='DERECHOHAB', null=True)),
                ('embarazo', models.TextField(blank=True, db_column='EMBARAZO', null=True)),
                ('rel_emba', models.TextField(blank=True, db_column='REL_EMBA', null=True)),
                ('horas', models.TextField(blank=True, db_column='HORAS', null=True)),
                ('minutos', models.TextField(blank=True, db_column='MINUTOS', null=True)),
                ('vio_fami', models.TextField(blank=True, db_column='VIO_FAMI', null=True)),
                ('area_ur', models.TextField(blank=True, db_column='AREA_UR', null=True)),
                ('edad_agru', models.TextField(blank=True, db_column='EDAD_AGRU', null=True)),
                ('lengua', models.TextField(blank=True, db_column='LENGUA', null=True)),
                ('cond_act', models.TextField(blank=True, db_column='COND_ACT', null=True)),
                ('agru_edad', models.TextField(blank=True, db_column='AGRU_EDAD', null=True)),
                ('edad_abs', models.TextField(blank=True, db_column='EDAD_ABS', null=True)),
            ],
            options={
                'db_table': 'CasosTotalRepublica',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='republica',
        ),
        migrations.DeleteModel(
            name='republicaV2',
        ),
    ]
