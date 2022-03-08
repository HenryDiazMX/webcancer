import csv
import pandas as pd
import folium
import plotly.express as px
import simplekml as simplekml
from django import forms
from django.shortcuts import render
from django.http import HttpResponse

from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def listascancer(request):
    municipios = republica.objects.order_by('mun_resid').all().distinct('mun_resid')
    localidades = republica.objects.order_by('loc_resid').all().distinct('loc_resid')
    años = republica.objects.order_by('anio_regis').all().distinct('anio_regis')
    tipoCancer = republica.objects.order_by('lista_mex').all().distinct('lista_mex')
    genero = republica.objects.order_by('sexo').all().distinct('sexo')
    estados = republica.objects.order_by('ent_resid').all().distinct('ent_resid')

    return render(request, "cancerinfantil/listas.html",
                  {"estados": estados, "municipios": municipios, "localidades": localidades, "años": años,
                   "cancer": tipoCancer, "genero": genero})


@csrf_exempt
def municipio(request):
    global tag, listaMunicipio, municipios, datos, idEstado, listaMunicipios
    if request.method == 'POST':
        idEstado = request.POST['idEstado']
        municipios = republica.objects.order_by('mun_resid').all().distinct('mun_resid').filter(ent_resid= idEstado )
        listaMunicipios = "<option value='TODOS'>TODOS</option>"
        for municipio in municipios:
            listaMunicipios = listaMunicipios + "<option value = '" + municipio.mun_resid + "'>" + municipio.mun_resid + "</option>"
    return HttpResponse(listaMunicipios)

@csrf_exempt
def localidad(request):
    global listaLocalidades
    if request.method == 'POST':
        idMunicipio = request.POST['idMunicipio']
        localidades = republica.objects.order_by('loc_resid').all().distinct('loc_resid').filter(mun_resid= idMunicipio )
        listaLocalidades = "<option value='TODOS'>TODOS</option>"
        for localidad in localidades:
            listaLocalidades = listaLocalidades + "<option value = '" + localidad.loc_resid + "'>" + localidad.loc_resid + "</option>"
    return HttpResponse(listaLocalidades)


def mapascancer(request):
    estados = republica.objects.distinct('ent_resid')
    municipios = republica.objects.distinct('mun_resid')
    localidades = republica.objects.distinct('loc_resid')
    años = republica.objects.distinct('anio_regis')
    tipoCancer = republica.objects.distinct('lista_mex')
    genero = republica.objects.distinct('sexo')
    edad = republica.objects.distinct('edad').order_by('edad')

    datos = guerrero.objects.all().values()

    df = pd.DataFrame(datos)

    datos2 = pd.DataFrame()
    for i in range(0, len(df)):
        datos2.loc[i, 'DESCRIPCION'] = "EDAD: " + str(df.loc[i, 'edad']) + ", " + "SEXO: " + df.loc[
            i, "sexo"] + ", " + "CAUSA/ENFERMEDAD: " + df.loc[i, "lista_mex"] + ", " + "OCURRENCIA: " + df.loc[
                                           i, "loc_ocurr"] + ", " + df.loc[i, "mun_ocurr"] + ", " + df.loc[
                                           i, "ent_ocurr"] + ", " + "LUGAR DE RESIDENCIA: " + df.loc[
                                           i, "loc_resid"] + ", " + df.loc[i, "mun_resid"] + ", " + df.loc[
                                           i, "ent_resid"]
        datos2.loc[i, 'longitud_ocurr'] = df.loc[i, 'longitud_ocurr']
        datos2.loc[i, 'latitud_ocurr'] = df.loc[i, 'latitud_ocurr']

    map = folium.Map(location=[datos2.latitud_ocurr.mean(), datos2.longitud_ocurr.mean()], zoom_start=8,
                     control_scale=False, min_zoom=5)

    for index, location_info in datos2.iterrows():
        folium.Marker([location_info["latitud_ocurr"], location_info["longitud_ocurr"]],
                      popup=location_info["DESCRIPCION"], icon=folium.Icon(icon="glyphicon-flag")).add_to(map)

    map = map._repr_html_()

    context = {
        'map': map,
        'df': df,
        "republica": estados, "estado": municipios, "municipio": localidades, "año": años,
        "cancer": tipoCancer, "genero": genero, "edad": edad
    }

    return render(request, "cancerinfantil/maps.html", context)


def graficascancer(request):
    datos = guerrero.objects.all().values()
    df = pd.DataFrame(datos)
    datos = republica.objects.all()

    estado = datos.filter()

    estados = republica.objects.distinct('ent_resid')
    municipios = republica.objects.distinct('mun_resid')
    localidades = republica.objects.distinct('loc_resid')
    años = republica.objects.distinct('anio_regis')
    tipoCancer = republica.objects.distinct('lista_mex')
    genero = republica.objects.distinct('sexo')

    datos2 = pd.DataFrame()
    for i in range(0, len(df)):
        datos2.loc[i, 'año'] = df.loc[i, 'anio_regis']
        datos2.loc[i, 'lista_mex'] = df.loc[i, 'lista_mex']
    value_counts = datos2.value_counts(sort=True)
    df_val_counts = pd.DataFrame(value_counts)
    datos3 = df_val_counts.reset_index()
    datos3.columns = ['AÑO', 'LISTA_MEX', 'CONTEO']  # change column names
    fig = px.pie(datos3, values='CONTEO', names='LISTA_MEX')
    fig.update_traces(hoverinfo='label+percent', textposition='inside')
    fig.update_layout(width=1200, height=600, uniformtext_minsize=12, uniformtext_mode='hide')

    fig = fig._repr_html_()

    return render(request, "cancerinfantil/graficaspreview.html",
                  {"fig": fig, "republica": estados, "estado": municipios, "municipio": localidades, "año": años,
                   "cancer": tipoCancer, "genero": genero, "df": df})


def export_csv(request):
    if request.method == 'POST':
        # query
        queryset = republica.objects.filter(ent_resid=request.POST['frmEstado'])

        # get fields of model
        options = republica._meta
        fields = [field.name for field in options.fields]

        # build response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'atachment; fieldname="CancerInfantil.csv"'
        # writer
        writer = csv.writer(response)
        # writer header
        writer.writerow([options.get_field(field).verbose_name for field in fields])
        # writing data
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in fields])

    return response


def generarkml(request):
    datos = guerrero.objects.all().values()
    df = pd.DataFrame(datos)
    datos1 = df
    datos2 = pd.DataFrame()
    for i in range(0, len(datos1)):
        datos2.loc[i, 'DESCRIPCIONRESID'] = "EDAD: " + str(datos1.loc[i, 'edad']) + ", " + "SEXO: " + datos1.loc[
            i, "sexo"] + ", " + "CAUSA/ENFERMEDAD: " + datos1.loc[i, "lista_mex"] + ", UBICACION: " + datos1.loc[
                                                i, "loc_resid"] + ", " + datos1.loc[i, "mun_resid"] + ", " + datos1.loc[
                                                i, "ent_resid"]
        datos2.loc[i, 'DESCRIPCIONOCURR'] = "EDAD: " + str(datos1.loc[i, 'edad']) + ", " + "SEXO: " + datos1.loc[
            i, "sexo"] + ", " + "CAUSA/ENFERMEDAD: " + datos1.loc[i, "lista_mex"] + ", OCURRENCIA: " + datos1.loc[
                                                i, "loc_ocurr"] + ", " + datos1.loc[i, "mun_ocurr"] + ", " + datos1.loc[
                                                i, "ent_ocurr"] + ", LUGAR DE RESIDENCIA: " + datos1.loc[
                                                i, "loc_resid"] + ", " + datos1.loc[i, "mun_resid"] + ", " + datos1.loc[
                                                i, "ent_resid"]
        datos2.loc[i, 'LONGITUD_RESID'] = datos1.loc[i, 'longitud_resid']
        datos2.loc[i, 'LATITUD_RESID'] = datos1.loc[i, 'latitud_resid']
        datos2.loc[i, 'LONGITUD_OCURR'] = datos1.loc[i, 'longitud_ocurr']
        datos2.loc[i, 'LATITUD_OCURR'] = datos1.loc[i, 'latitud_ocurr']
        datos2.loc[i, 'ANIO_REGIS'] = datos1.loc[i, 'anio_regis']
        pass

    datos2['CASO'] = datos2.index + 1
    for i in range(0, len(datos1)):
        datos2.loc[i, 'NAME'] = '#' + str(datos2.loc[i, 'CASO']) + " " + str(datos1.loc[i, 'anio_regis'])
        pass

    a15 = datos2['ANIO_REGIS'] == 2015
    datos15 = datos2[a15]
    a16 = datos2['ANIO_REGIS'] == 2016
    datos16 = datos2[a16]
    a17 = datos2['ANIO_REGIS'] == 2017
    datos17 = datos2[a17]
    a18 = datos2['ANIO_REGIS'] == 2018
    datos18 = datos2[a18]
    a19 = datos2['ANIO_REGIS'] == 2019
    datos19 = datos2[a19]
    a20 = datos2['ANIO_REGIS'] == 2020
    datos20 = datos2[a20]

    points_kml = simplekml.Kml()

    lolabelsRes = points_kml.newfolder(name="Residencia")
    lolabelsOcurr = points_kml.newfolder(name="Ocurrencia")
    lolabelsRes15 = lolabelsRes.newfolder(name="Año 2015")
    lolabelsRes16 = lolabelsRes.newfolder(name="Año 2016")
    lolabelsRes17 = lolabelsRes.newfolder(name="Año 2017")
    lolabelsRes18 = lolabelsRes.newfolder(name="Año 2018")
    lolabelsRes19 = lolabelsRes.newfolder(name="Año 2019")
    lolabelsRes20 = lolabelsRes.newfolder(name="Año 2020")

    lolabelsOcurr15 = lolabelsOcurr.newfolder(name="Año 2015")
    lolabelsOcurr16 = lolabelsOcurr.newfolder(name="Año 2016")
    lolabelsOcurr17 = lolabelsOcurr.newfolder(name="Año 2017")
    lolabelsOcurr18 = lolabelsOcurr.newfolder(name="Año 2018")
    lolabelsOcurr19 = lolabelsOcurr.newfolder(name="Año 2019")
    lolabelsOcurr20 = lolabelsOcurr.newfolder(name="Año 2020")

    style1 = simplekml.Style()
    style1.iconstyle.color = 'ff90ee90'
    style1.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/flag.png'
    style1.iconstyle.scale = 1

    style2 = simplekml.Style()
    style2.iconstyle.color = 'FFD4FF7F'
    style2.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/flag.png'
    style2.iconstyle.scale = 1

    style3 = simplekml.Style()
    style3.iconstyle.color = 'FF3C14DC'
    style3.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/flag.png'
    style3.iconstyle.scale = 1

    style4 = simplekml.Style()
    style4.iconstyle.color = 'FF00D7FF'
    style4.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/flag.png'
    style4.iconstyle.scale = 1

    style5 = simplekml.Style()
    style5.iconstyle.color = 'FF800080'
    style5.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/flag.png'
    style5.iconstyle.scale = 1

    for i in datos15.itertuples():
        lo = lolabelsRes15.newpoint(name=i.NAME, description=i.DESCRIPCIONRESID,
                                    coords=[(i.LONGITUD_RESID, i.LATITUD_RESID)])
        lo.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/blu-circle.png'
        lo = lolabelsOcurr15.newpoint(name=i.NAME, description=i.DESCRIPCIONOCURR,
                                      coords=[(i.LONGITUD_OCURR, i.LATITUD_OCURR)])
        lo.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/flag.png'

    for i in datos16.itertuples():
        lo = lolabelsRes16.newpoint(name=i.NAME, description=i.DESCRIPCIONRESID,
                                    coords=[(i.LONGITUD_RESID, i.LATITUD_RESID)])
        lo.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/grn-circle.png'
        lo = lolabelsOcurr16.newpoint(name=i.NAME, description=i.DESCRIPCIONOCURR,
                                      coords=[(i.LONGITUD_OCURR, i.LATITUD_OCURR)])
        lo.style = style1

    for i in datos17.itertuples():
        lo = lolabelsRes17.newpoint(name=i.NAME, description=i.DESCRIPCIONRESID,
                                    coords=[(i.LONGITUD_RESID, i.LATITUD_RESID)])
        lo.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/ltblu-circle.png'
        lo = lolabelsOcurr17.newpoint(name=i.NAME, description=i.DESCRIPCIONOCURR,
                                      coords=[(i.LONGITUD_OCURR, i.LATITUD_OCURR)])
        lo.style = style2

    for i in datos18.itertuples():
        lo = lolabelsRes18.newpoint(name=i.NAME, description=i.DESCRIPCIONRESID,
                                    coords=[(i.LONGITUD_RESID, i.LATITUD_RESID)])
        lo.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/red-circle.png'
        lo = lolabelsOcurr18.newpoint(name=i.NAME, description=i.DESCRIPCIONOCURR,
                                      coords=[(i.LONGITUD_OCURR, i.LATITUD_OCURR)])
        lo.style = style3

    for i in datos19.itertuples():
        lo = lolabelsRes19.newpoint(name=i.NAME, description=i.DESCRIPCIONRESID,
                                    coords=[(i.LONGITUD_RESID, i.LATITUD_RESID)])
        lo.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png'
        lo = lolabelsOcurr19.newpoint(name=i.NAME, description=i.DESCRIPCIONOCURR,
                                      coords=[(i.LONGITUD_OCURR, i.LATITUD_OCURR)])
        lo.style = style4

    for i in datos20.itertuples():
        lo = lolabelsRes20.newpoint(name=i.NAME, description=i.DESCRIPCIONRESID,
                                    coords=[(i.LONGITUD_RESID, i.LATITUD_RESID)])
        lo.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/purple-circle.png'
        lo = lolabelsOcurr20.newpoint(name=i.NAME, description=i.DESCRIPCIONOCURR,
                                      coords=[(i.LONGITUD_OCURR, i.LATITUD_OCURR)])
        lo.style = style5

    response = HttpResponse(points_kml.kml())
    response['Content-Disposition'] = 'attachment; filename="Mapa.kml"'
    response['Content-Type'] = 'application/kml'

    return response
