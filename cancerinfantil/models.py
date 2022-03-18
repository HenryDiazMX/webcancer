from django.db import models


# Create your models here.

class republicaapi(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ent_regis = models.TextField(db_column='ENT_REGIS', blank=True, null=True)  # Field name made lowercase.
    mun_regis = models.TextField(db_column='MUN_REGIS', blank=True, null=True)  # Field name made lowercase.
    ent_resid = models.TextField(db_column='ENT_RESID', blank=True, null=True)  # Field name made lowercase.
    mun_resid = models.TextField(db_column='MUN_RESID', blank=True, null=True)  # Field name made lowercase.
    tloc_resid = models.TextField(db_column='TLOC_RESID', blank=True, null=True)  # Field name made lowercase.
    loc_resid = models.TextField(db_column='LOC_RESID', blank=True, null=True)  # Field name made lowercase.
    latitud_resid = models.FloatField(db_column='LATITUD_RESID', blank=True, null=True)  # Field name made lowercase.
    longitud_resid = models.FloatField(db_column='LONGITUD_RESID', blank=True, null=True)  # Field name made lowercase.
    coincidencia_resid = models.TextField(db_column='COINCIDENCIA_RESID', blank=True, null=True)  # Field name made lowercase.
    ent_ocurr = models.TextField(db_column='ENT_OCURR', blank=True, null=True)  # Field name made lowercase.
    mun_ocurr = models.TextField(db_column='MUN_OCURR', blank=True, null=True)  # Field name made lowercase.
    tloc_ocurr = models.TextField(db_column='TLOC_OCURR', blank=True, null=True)  # Field name made lowercase.
    loc_ocurr = models.TextField(db_column='LOC_OCURR', blank=True, null=True)  # Field name made lowercase.
    latitud_ocurr = models.FloatField(db_column='LATITUD_OCURR', blank=True, null=True)  # Field name made lowercase.
    longitud_ocurr = models.FloatField(db_column='LONGITUD_OCURR', blank=True, null=True)  # Field name made lowercase.
    coincidencia_ocurr = models.TextField(db_column='COINCIDENCIA_OCURR', blank=True, null=True)  # Field name made lowercase.
    causa_def = models.TextField(db_column='CAUSA_DEF', blank=True, null=True)  # Field name made lowercase.
    lista_mex = models.TextField(db_column='LISTA_MEX', blank=True, null=True)  # Field name made lowercase.
    sexo = models.TextField(db_column='SEXO', blank=True, null=True)  # Field name made lowercase.
    edad = models.TextField(db_column='EDAD', blank=True, null=True)  # Field name made lowercase.
    dia_ocurr = models.TextField(db_column='DIA_OCURR', blank=True, null=True)  # Field name made lowercase.
    mes_ocurr = models.TextField(db_column='MES_OCURR', blank=True, null=True)  # Field name made lowercase.
    anio_ocur = models.BigIntegerField(db_column='ANIO_OCUR', blank=True, null=True)  # Field name made lowercase.
    dia_regis = models.TextField(db_column='DIA_REGIS', blank=True, null=True)  # Field name made lowercase.
    mes_regis = models.TextField(db_column='MES_REGIS', blank=True, null=True)  # Field name made lowercase.
    anio_regis = models.BigIntegerField(db_column='ANIO_REGIS', blank=True, null=True)  # Field name made lowercase.
    dia_nacim = models.TextField(db_column='DIA_NACIM', blank=True, null=True)  # Field name made lowercase.
    mes_nacim = models.TextField(db_column='MES_NACIM', blank=True, null=True)  # Field name made lowercase.
    anio_nacim = models.TextField(db_column='ANIO_NACIM', blank=True, null=True)  # Field name made lowercase.
    ocupacion = models.TextField(db_column='OCUPACION', blank=True, null=True)  # Field name made lowercase.
    escolarida = models.TextField(db_column='ESCOLARIDA', blank=True, null=True)  # Field name made lowercase.
    edo_civil = models.TextField(db_column='EDO_CIVIL', blank=True, null=True)  # Field name made lowercase.
    necropsia = models.TextField(db_column='NECROPSIA', blank=True, null=True)  # Field name made lowercase.
    asist_medi = models.TextField(db_column='ASIST_MEDI', blank=True, null=True)  # Field name made lowercase.
    sitio_ocur = models.TextField(db_column='SITIO_OCUR', blank=True, null=True)  # Field name made lowercase.
    cond_cert = models.TextField(db_column='COND_CERT', blank=True, null=True)  # Field name made lowercase.
    nacionalid = models.TextField(db_column='NACIONALID', blank=True, null=True)  # Field name made lowercase.
    derechohab = models.TextField(db_column='DERECHOHAB', blank=True, null=True)  # Field name made lowercase.
    embarazo = models.TextField(db_column='EMBARAZO', blank=True, null=True)  # Field name made lowercase.
    rel_emba = models.TextField(db_column='REL_EMBA', blank=True, null=True)  # Field name made lowercase.
    horas = models.TextField(db_column='HORAS', blank=True, null=True)  # Field name made lowercase.
    minutos = models.TextField(db_column='MINUTOS', blank=True, null=True)  # Field name made lowercase.
    vio_fami = models.TextField(db_column='VIO_FAMI', blank=True, null=True)  # Field name made lowercase.
    area_ur = models.TextField(db_column='AREA_UR', blank=True, null=True)  # Field name made lowercase.
    edad_agru = models.TextField(db_column='EDAD_AGRU', blank=True, null=True)  # Field name made lowercase.
    lengua = models.TextField(db_column='LENGUA', blank=True, null=True)  # Field name made lowercase.
    cond_act = models.TextField(db_column='COND_ACT', blank=True, null=True)  # Field name made lowercase.
    agru_edad = models.TextField(db_column='AGRU_EDAD', blank=True, null=True)  # Field name made lowercase.
    fecha_verificacion = models.TextField(db_column='FECHA_VERIFICACION', blank=True, null=True)  # Field name made lowercase.
    nombre_verificador = models.TextField(db_column='NOMBRE_VERIFICADOR', blank=True, null=True)  # Field name made lowercase.
    edad_abs = models.TextField(db_column='EDAD_ABS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CasosRepublicaMex'


class republica(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ent_regis = models.TextField(db_column='ENT_REGIS', blank=True, null=True)  # Field name made lowercase.
    mun_regis = models.TextField(db_column='MUN_REGIS', blank=True, null=True)  # Field name made lowercase.
    ent_resid = models.TextField(db_column='ENT_RESID', blank=True, null=True)  # Field name made lowercase.
    mun_resid = models.TextField(db_column='MUN_RESID', blank=True, null=True)  # Field name made lowercase.
    tloc_resid = models.TextField(db_column='TLOC_RESID', blank=True, null=True)  # Field name made lowercase.
    loc_resid = models.TextField(db_column='LOC_RESID', blank=True, null=True)  # Field name made lowercase.
    latitud_resid = models.FloatField(db_column='LATITUD_RESID', blank=True, null=True)  # Field name made lowercase.
    longitud_resid = models.FloatField(db_column='LONGITUD_RESID', blank=True, null=True)  # Field name made lowercase.
    ent_ocurr = models.TextField(db_column='ENT_OCURR', blank=True, null=True)  # Field name made lowercase.
    mun_ocurr = models.TextField(db_column='MUN_OCURR', blank=True, null=True)  # Field name made lowercase.
    tloc_ocurr = models.TextField(db_column='TLOC_OCURR', blank=True, null=True)  # Field name made lowercase.
    loc_ocurr = models.TextField(db_column='LOC_OCURR', blank=True, null=True)  # Field name made lowercase.
    latitud_ocurr = models.FloatField(db_column='LATITUD_OCURR', blank=True, null=True)  # Field name made lowercase.
    longitud_ocurr = models.FloatField(db_column='LONGITUD_OCURR', blank=True, null=True)  # Field name made lowercase.
    causa_def = models.TextField(db_column='CAUSA_DEF', blank=True, null=True)  # Field name made lowercase.
    lista_mex = models.TextField(db_column='LISTA_MEX', blank=True, null=True)  # Field name made lowercase.
    sexo = models.TextField(db_column='SEXO', blank=True, null=True)  # Field name made lowercase.
    edad = models.TextField(db_column='EDAD', blank=True, null=True)  # Field name made lowercase.
    dia_ocurr = models.TextField(db_column='DIA_OCURR', blank=True, null=True)  # Field name made lowercase.
    mes_ocurr = models.TextField(db_column='MES_OCURR', blank=True, null=True)  # Field name made lowercase.
    anio_ocur = models.BigIntegerField(db_column='ANIO_OCUR', blank=True, null=True)  # Field name made lowercase.
    dia_regis = models.TextField(db_column='DIA_REGIS', blank=True, null=True)  # Field name made lowercase.
    mes_regis = models.TextField(db_column='MES_REGIS', blank=True, null=True)  # Field name made lowercase.
    anio_regis = models.BigIntegerField(db_column='ANIO_REGIS', blank=True, null=True)  # Field name made lowercase.
    dia_nacim = models.TextField(db_column='DIA_NACIM', blank=True, null=True)  # Field name made lowercase.
    mes_nacim = models.TextField(db_column='MES_NACIM', blank=True, null=True)  # Field name made lowercase.
    anio_nacim = models.TextField(db_column='ANIO_NACIM', blank=True, null=True)  # Field name made lowercase.
    ocupacion = models.TextField(db_column='OCUPACION', blank=True, null=True)  # Field name made lowercase.
    escolarida = models.TextField(db_column='ESCOLARIDA', blank=True, null=True)  # Field name made lowercase.
    edo_civil = models.TextField(db_column='EDO_CIVIL', blank=True, null=True)  # Field name made lowercase.
    necropsia = models.TextField(db_column='NECROPSIA', blank=True, null=True)  # Field name made lowercase.
    asist_medi = models.TextField(db_column='ASIST_MEDI', blank=True, null=True)  # Field name made lowercase.
    sitio_ocur = models.TextField(db_column='SITIO_OCUR', blank=True, null=True)  # Field name made lowercase.
    cond_cert = models.TextField(db_column='COND_CERT', blank=True, null=True)  # Field name made lowercase.
    nacionalid = models.TextField(db_column='NACIONALID', blank=True, null=True)  # Field name made lowercase.
    derechohab = models.TextField(db_column='DERECHOHAB', blank=True, null=True)  # Field name made lowercase.
    embarazo = models.TextField(db_column='EMBARAZO', blank=True, null=True)  # Field name made lowercase.
    rel_emba = models.TextField(db_column='REL_EMBA', blank=True, null=True)  # Field name made lowercase.
    horas = models.TextField(db_column='HORAS', blank=True, null=True)  # Field name made lowercase.
    minutos = models.TextField(db_column='MINUTOS', blank=True, null=True)  # Field name made lowercase.
    vio_fami = models.TextField(db_column='VIO_FAMI', blank=True, null=True)  # Field name made lowercase.
    area_ur = models.TextField(db_column='AREA_UR', blank=True, null=True)  # Field name made lowercase.
    edad_agru = models.TextField(db_column='EDAD_AGRU', blank=True, null=True)  # Field name made lowercase.
    lengua = models.TextField(db_column='LENGUA', blank=True, null=True)  # Field name made lowercase.
    cond_act = models.TextField(db_column='COND_ACT', blank=True, null=True)  # Field name made lowercase.
    agru_edad = models.TextField(db_column='AGRU_EDAD', blank=True, null=True)  # Field name made lowercase.
    edad_abs = models.TextField(db_column='EDAD_ABS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Casostocsv'
