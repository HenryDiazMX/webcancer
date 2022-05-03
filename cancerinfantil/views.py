import codecs
import csv
import time
import pandas as pd
import folium
import plotly.express as px
import simplekml as simplekml
from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse

from webcancer import settings
from .models import *
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# Generacion de la pagina de listas, llamando a los datos de la base
@csrf_exempt
def listascancer(request):
    estados = Casostotalrepublica.objects.order_by('ent_resid').all().distinct('ent_resid')
    municipios = Casostotalrepublica.objects.order_by('mun_resid').all().distinct('mun_resid')
    localidades = Casostotalrepublica.objects.order_by('loc_resid').all().distinct('loc_resid')
    anios = Casostotalrepublica.objects.order_by('anio_regis').all().distinct('anio_regis')
    tipoCancer = Casostotalrepublica.objects.order_by('lista_mex').all().distinct('lista_mex')
    genero = Casostotalrepublica.objects.order_by('sexo').all().distinct('sexo')
    agruedad = Casostotalrepublica.objects.distinct('agru_edad')

    return render(request, "cancerinfantil/listas.html",
                  {"estados": estados, "municipios": municipios, "localidades": localidades, "años": anios,
                   "cancer": tipoCancer, "genero": genero, "agruedad": agruedad})


# Obtencion del Municipio de acuerdo al Estado realizado en un JavaScript
@csrf_exempt
def municipio(request):
    global listaMunicipios
    if request.method == 'POST':
        idEstado = request.POST['idEstado']
        municipios = republicaapi.objects.order_by('mun_resid').all().distinct('mun_resid').filter(ent_resid=idEstado)
        listaMunicipios = "<option value='TODOS'>TODOS</option>"
        for municipio in municipios:
            listaMunicipios = listaMunicipios + "<option value = '" + municipio.mun_resid + "'>" + municipio.mun_resid.upper() + "</option>"
    return HttpResponse(listaMunicipios)


# Obtencion de la Localidad de acuerdo al Municipio realizado en un JavaScript
@csrf_exempt
def localidad(request):
    global listaLocalidades
    if request.method == 'POST':
        idMunicipio = request.POST['idMunicipio']
        localidades = republicaapi.objects.order_by('loc_resid').all().distinct('loc_resid').filter(
            mun_resid=idMunicipio)
        listaLocalidades = "<option value='TODOS'>TODOS</option>"
        for localidad in localidades:
            listaLocalidades = listaLocalidades + "<option value = '" + localidad.loc_resid + "'>" + localidad.loc_resid.upper() + "</option>"
    return HttpResponse(listaLocalidades)


# Obtencion del Municipio de acuerdo al Estado en la vista de listas y graficas
@csrf_exempt
def municipio2(request):
    global listaMunicipios
    if request.method == 'POST':
        idEstado = request.POST['idEstado']
        municipios = Casostotalrepublica.objects.order_by('mun_resid').all().distinct('mun_resid').filter(ent_resid=idEstado)
        listaMunicipios = "<option value='TODOS'>TODOS</option>"
        for municipio in municipios:
            listaMunicipios = listaMunicipios + "<option value = '" + municipio.mun_resid + "'>" + municipio.mun_resid.upper() + "</option>"
    return HttpResponse(listaMunicipios)


# Obtencion de la Localidad de acuerdo al Municipio en la vista de listas y graficas
@csrf_exempt
def localidad2(request):
    global listaLocalidades
    if request.method == 'POST':
        idMunicipio = request.POST['idMunicipio']
        localidades = Casostotalrepublica.objects.order_by('loc_resid').all().distinct('loc_resid').filter(
            mun_resid=idMunicipio)
        listaLocalidades = "<option value='TODOS'>TODOS</option>"
        for localidad in localidades:
            listaLocalidades = listaLocalidades + "<option value = '" + localidad.loc_resid + "'>" + localidad.loc_resid.upper() + "</option>"
    return HttpResponse(listaLocalidades)


def get_headers():
    return ['id', 'ent_regis', 'mun_regis', 'ent_resid', 'mun_resid', 'tloc_resid', 'loc_resid', 'ent_ocurr',
            'mun_ocurr', 'tloc_ocurr', 'loc_ocurr', 'causa_def', 'lista_mex', 'sexo', 'edad', 'dia_ocurr', 'mes_ocurr',
            'anio_ocur', 'dia_regis', 'mes_regis', 'anio_regis', 'dia_nacim', 'mes_nacim', 'anio_nacim', 'ocupacion',
            'escolarida', 'edo_civil', 'necropsia', 'asist_medi', 'sitio_ocur', 'cond_cert', 'nacionalid', 'derechohab',
            'embarazo', 'rel_emba', 'horas', 'minutos', 'vio_fami', 'area_ur', 'edad_agru', 'lengua', 'cond_act',
            'agru_edad', 'edad_abs']

def get_data(data):
    return {
        'id': data.id,
        'ent_regis': data.ent_regis,
        'mun_regis': data.mun_regis,
        'ent_resid': data.ent_resid,
        'mun_resid': data.mun_resid,
        'tloc_resid': data.tloc_resid,
        'loc_resid': data.loc_resid,
        'ent_ocurr': data.ent_ocurr,
        'mun_ocurr': data.mun_ocurr,
        'tloc_ocurr': data.tloc_ocurr,
        'loc_ocurr': data.loc_ocurr,
        'causa_def': data.causa_def,
        'lista_mex': data.lista_mex,
        'sexo': data.sexo,
        'edad': data.edad,
        'dia_ocurr': data.dia_ocurr,
        'mes_ocurr': data.mes_ocurr,
        'anio_ocur': data.anio_ocur,
        'dia_regis': data.dia_regis,
        'mes_regis': data.mes_regis,
        'anio_regis': data.anio_regis,
        'dia_nacim': data.dia_nacim,
        'mes_nacim': data.mes_nacim,
        'anio_nacim': data.anio_nacim,
        'ocupacion': data.ocupacion,
        'escolarida': data.escolarida,
        'edo_civil': data.edo_civil,
        'necropsia': data.necropsia,
        'asist_medi': data.asist_medi,
        'sitio_ocur': data.sitio_ocur,
        'cond_cert': data.cond_cert,
        'nacionalid': data.nacionalid,
        'derechohab': data.derechohab,
        'embarazo': data.embarazo,
        'rel_emba': data.rel_emba,
        'horas': data.horas,
        'minutos': data.minutos,
        'vio_fami': data.vio_fami,
        'area_ur': data.area_ur,
        'edad_agru': data.edad_agru,
        'lengua': data.lengua,
        'cond_act': data.cond_act,
        'agru_edad': data.agru_edad,
        'edad_abs' : data.edad_abs
    }

# StreamingHttpResponse requires a File-like class that has a 'write' method
class Echo(object):
    def write(self, value):
        return value

def iter_items(datas, pseudo_buffer):
    yield pseudo_buffer.write(codecs.BOM_UTF8)
    writer = csv.DictWriter(pseudo_buffer, fieldnames=get_headers())
    yield writer.writeheader()

    for data in datas:
        yield writer.writerow(get_data(data))

def get_response(iterator):
    response = StreamingHttpResponse(
        streaming_content=(iter_items(iterator, Echo())),
        content_type='text/csv',
    )
    response['Content-Disposition'] = 'attachment;filename=CasosCancer.csv'
    return response

@csrf_exempt
def export_csv(request):
    global queryset, response, df
    if request.method == 'POST':
        # 1. Get the iterator of the QuerySet
        queryset = Casostotalrepublica.objects.all()
        queryset = queryset.order_by('id')
        if request.POST['frmEstado'] != "TODOS":
            queryset = queryset.filter(ent_resid=request.POST['frmEstado'])
            if request.POST['frmMunicipio'] != "TODOS":
                queryset = queryset.filter(mun_resid=request.POST['frmMunicipio'])
                if request.POST["frmLocalidad"] != "TODOS":
                    queryset = queryset.filter(loc_resid=request.POST['frmLocalidad'])
        if request.POST['frmRangoEdad'] != "TODOS":
            queryset = queryset.filter(agru_edad=request.POST['frmRangoEdad'])
        if request.POST['frmRegistro'] != "TODOS":
            queryset = queryset.filter(anio_regis=request.POST['frmRegistro'])
        if request.POST['frmCancer'] != "TODOS":
            queryset = queryset.filter(lista_mex=request.POST['frmCancer'])
        if request.POST['frmGenero'] != "TODOS":
            queryset = queryset.filter(sexo=request.POST['frmGenero'])

        iterator = queryset.iterator()

        return get_response(iterator)


# Generacion de la vista inicial de la pagina de Mapas, genera el mapa sin casos, al hacer un POST toma los datos para hacer filtros
@csrf_exempt
def mapascancer(request):
    div = ""
    estados = republicaapi.objects.distinct('ent_resid')
    municipios = republicaapi.objects.distinct('mun_resid')
    localidades = republicaapi.objects.distinct('loc_resid')
    anios = republicaapi.objects.distinct('anio_regis')
    tipoCancer = republicaapi.objects.distinct('lista_mex')
    genero = republicaapi.objects.distinct('sexo')
    agruedad = republicaapi.objects.distinct('agru_edad')
    global map, response, respuesta
    map = folium.Map(location=[24.492393, -101.787064], zoom_start=5, control_scale=False, min_zoom=5)
    map = map._repr_html_()

    queryset = republicaapi.objects.all().values()
    if request.method == 'POST':
        try:
            # query
            if request.POST['frmEstado'] != "TODOS":
                queryset = queryset.filter(ent_resid=request.POST['frmEstado'])
                if request.POST['frmMunicipio'] != "TODOS":
                    queryset = queryset.filter(mun_resid=request.POST['frmMunicipio'])
                    if request.POST["frmLocalidad"] != "TODOS":
                        queryset = queryset.filter(loc_resid=request.POST['frmLocalidad'])

            if request.POST['frmCancer'] != "TODOS":
                queryset = queryset.filter(lista_mex=request.POST['frmCancer'])
            if request.POST['frmRegistro'] != "TODOS":
                queryset = queryset.filter(anio_regis=request.POST['frmRegistro'])
            if request.POST['frmRangoEdad'] != "TODOS":
                queryset = queryset.filter(agru_edad=request.POST['frmRangoEdad'])
            if request.POST['frmGenero'] != "TODOS":
                queryset = queryset.filter(sexo=request.POST['frmGenero'])
            # get fields of model
            df = pd.DataFrame(queryset)
            datos3 = pd.DataFrame()
            for i in range(0, len(df)):
                datos3.loc[i, 'DESCRIPCION'] = "EDAD: " + str(df.loc[i, 'edad']) + ", " + "SEXO: " + df.loc[
                    i, "sexo"] + ", " + "CAUSA/ENFERMEDAD: " + df.loc[i, "lista_mex"] + ", " + "OCURRENCIA: " + df.loc[
                                                   i, "loc_ocurr"] + ", " + df.loc[i, "mun_ocurr"] + ", " + df.loc[
                                                   i, "ent_ocurr"] + ", " + "LUGAR DE RESIDENCIA: " + df.loc[
                                                   i, "loc_resid"] + ", " + df.loc[i, "mun_resid"] + ", " + df.loc[
                                                   i, "ent_resid"]
                datos3.loc[i, 'longitud_ocurr'] = df.loc[i, 'longitud_ocurr']
                datos3.loc[i, 'latitud_ocurr'] = df.loc[i, 'latitud_ocurr']
                datos3.loc[i, 'longitud_resid'] = df.loc[i, 'longitud_resid']
                datos3.loc[i, 'latitud_resid'] = df.loc[i, 'latitud_resid']

            if request.POST['frmTipoRegistro'] == "OCURRENCIA":
                if request.POST['frmTipoMapa'] == "PLANO":
                    map = folium.Map(location=[datos3.latitud_ocurr.mean(), datos3.longitud_ocurr.mean()],
                                     zoom_start=7.5,
                                     control_scale=False, min_zoom=5)
                else:
                    map = folium.Map(location=[datos3.latitud_ocurr.mean(), datos3.longitud_ocurr.mean()],
                                     zoom_start=7.5,
                                     control_scale=False, min_zoom=5, tiles="Stamen Terrain")
                for index, location_info in datos3.iterrows():
                    folium.Marker([location_info["latitud_ocurr"], location_info["longitud_ocurr"]],
                                  popup=location_info["DESCRIPCION"], icon=folium.Icon(icon="glyphicon-flag")).add_to(
                        map)

            else:
                if request.POST['frmTipoMapa'] == "PLANO":
                    map = folium.Map(location=[datos3.latitud_resid.mean(), datos3.longitud_resid.mean()],
                                     zoom_start=7.5,
                                     control_scale=False, min_zoom=5)
                else:
                    map = folium.Map(location=[datos3.latitud_resid.mean(), datos3.longitud_resid.mean()],
                                     zoom_start=7.5,
                                     control_scale=False, min_zoom=5, tiles="Stamen Terrain")
                for index, location_info in datos3.iterrows():
                    folium.Marker([location_info["latitud_resid"], location_info["longitud_resid"]],
                                  popup=location_info["DESCRIPCION"], icon=folium.Icon(icon="glyphicon-flag")).add_to(
                        map)
            map = map._repr_html_()

            if 'btnDescargar' in request.POST:
                datos1 = df
                datos2 = pd.DataFrame()
                for i in range(0, len(datos1)):
                    datos2.loc[i, 'DESCRIPCIONRESID'] = "EDAD: " + str(datos1.loc[i, 'edad']) + ", " + "SEXO: " + \
                                                        datos1.loc[
                                                            i, "sexo"] + ", " + "CAUSA/ENFERMEDAD: " + datos1.loc[
                                                            i, "lista_mex"] + ", UBICACION: " + datos1.loc[
                                                            i, "loc_resid"] + ", " + datos1.loc[i, "mun_resid"] + ", " + \
                                                        datos1.loc[
                                                            i, "ent_resid"]
                    datos2.loc[i, 'DESCRIPCIONOCURR'] = "EDAD: " + str(datos1.loc[i, 'edad']) + ", " + "SEXO: " + \
                                                        datos1.loc[
                                                            i, "sexo"] + ", " + "CAUSA/ENFERMEDAD: " + datos1.loc[
                                                            i, "lista_mex"] + ", OCURRENCIA: " + datos1.loc[
                                                            i, "loc_ocurr"] + ", " + datos1.loc[i, "mun_ocurr"] + ", " + \
                                                        datos1.loc[
                                                            i, "ent_ocurr"] + ", LUGAR DE RESIDENCIA: " + datos1.loc[
                                                            i, "loc_resid"] + ", " + datos1.loc[i, "mun_resid"] + ", " + \
                                                        datos1.loc[
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
                response['Content-Disposition'] = 'attachment; filename="MapaCasosCancerInfantil.kml"'
                response['Content-Type'] = 'application/kml'

        except AttributeError:
            div = "Su consulta no tiene casos para mostrar, realice otra consulta"

    context = {
        'map': map,
        "republica": estados, "estado": municipios, "municipio": localidades, "año": anios,
        "cancer": tipoCancer, "genero": genero, "agruedad": agruedad,
        "div": div,
    }
    try:
        if 'bntConsultar' in request.POST:
            respuesta = render(request, "cancerinfantil/maps.html", context)
        elif 'btnDescargar' in request.POST:
            respuesta = response
        else:
            respuesta = render(request, "cancerinfantil/maps.html", context)
    except NameError:
        div = "Su consulta no tiene casos para mostrar, realice otra consulta"

    return respuesta


@csrf_exempt
def graficascancer(request):
    global fig1
    datos = Casostotalrepublica.objects.all().values('id','ent_resid','lista_mex','sexo','edad_abs','anio_regis','sitio_ocur','area_ur','agru_edad')
    estados = Casostotalrepublica.objects.distinct('ent_resid')
    anios = Casostotalrepublica.objects.distinct('anio_regis')
    agruedad = Casostotalrepublica.objects.distinct('agru_edad')
    df = None
    tipoGrafica = ['CANCER DOMINANTES','SITIO DE OCURRENCIA', 'TIPO DE ÁREA', 'GENERO', 'EDAD']
    fig = ""
    texto = ""
    div = ""
    defaultEstado = ""
    defaultTipo = ""
    defaultAnio = ""
    defaultRango = ""
    try:
        if request.method == 'POST':
            if request.POST['frmEstado'] != "TODOS":
                datos = datos.filter(ent_resid=request.POST['frmEstado'])
                defaultEstado = request.POST['frmEstado']
            if request.POST['frmAnio'] != "TODOS":
                datos = datos.filter(anio_regis=request.POST['frmAnio'])
                defaultAnio = request.POST['frmAnio']
            if request.POST['frmRangoEdad'] != "TODOS":
                datos = datos.filter(agru_edad=request.POST['frmRangoEdad'])
                defaultRango = request.POST['frmRangoEdad']

            df = pd.DataFrame(datos)

            if request.POST['frmTipo'] == "CANCER DOMINANTES":
                defaultTipo = request.POST['frmTipo']
                datos2 = (df[['anio_regis', 'lista_mex']])
                value_counts = datos2.value_counts()
                df_val_counts = pd.DataFrame(value_counts)
                datos3 = df_val_counts.reset_index()
                datos3.columns = ['Año', 'Tipo De Cancer', 'Conteo']  # change column names
                fig1 = px.pie(datos3, values='Conteo', names='Tipo De Cancer')
                fig1.update_traces(hoverinfo='label+percent', textposition='inside')
                fig1.update_layout(autosize=True, uniformtext_minsize=16, uniformtext_mode='hide',
                                   legend_itemsizing="constant")
                texto = "Gráfica de los tipos de Cáncer Dominantes"
            if request.POST['frmTipo'] == "GENERO":
                defaultTipo = request.POST['frmTipo']
                datos2 = (df[['anio_regis', 'sexo']])
                value_counts = datos2.value_counts()
                df_val_counts = pd.DataFrame(value_counts)
                datos3 = df_val_counts.reset_index()
                datos3.columns = ['AÑO', 'SEXO', 'CONTEO']  # change column names
                fig1 = px.bar(datos3, x="AÑO", y="CONTEO", color="SEXO", height=700)
                texto = "Gráficas por Año de Registro y Genero"
            if request.POST['frmTipo'] == "SITIO DE OCURRENCIA":
                defaultTipo = request.POST['frmTipo']
                datos2 = (df[['sitio_ocur']])
                value_counts = datos2.value_counts()
                df_val_counts = pd.DataFrame(value_counts)
                datos3 = df_val_counts.reset_index()
                datos3.columns = ['SITIO DE OCURRENCIA', 'CONTEO']  # change column names
                fig1 = px.bar(datos3, x="SITIO DE OCURRENCIA", y="CONTEO", color='SITIO DE OCURRENCIA', text="CONTEO",
                              height=700)
                fig1.update_traces(textposition='outside')
                fig1.update_layout(uniformtext_minsize=1, uniformtext_mode='hide', showlegend=False)
                texto = "Lugares de Ocurrencia"
            if request.POST['frmTipo'] == "TIPO DE ÁREA":
                defaultTipo = request.POST['frmTipo']
                datos2 = (df[['anio_regis', 'area_ur']])
                value_counts = datos2.value_counts()
                df_val_counts = pd.DataFrame(value_counts)
                datos3 = df_val_counts.reset_index()
                datos3.columns = ['AÑO', 'TIPO DE AREA', 'CONTEO']  # change column names
                fig1 = px.bar(datos3, x="AÑO", y="CONTEO", color="TIPO DE AREA", height=700)
                texto = "Tipo de Área donde Residía el Niño(a)"
            if request.POST['frmTipo'] == "EDAD":
                defaultTipo = request.POST['frmTipo']
                datos2 = (df[['edad_abs']])
                value_counts = datos2.value_counts()
                df_val_counts = pd.DataFrame(value_counts)
                datos3 = df_val_counts.reset_index()
                datos3.columns = ['EDAD', 'CONTEO']  # change column names
                fig1 = px.bar(datos3, x="EDAD", y="CONTEO", color='EDAD', text="CONTEO", height=700)
                fig1.update_traces(textposition='outside')
                fig1.update_layout(uniformtext_minsize=7, uniformtext_mode='hide', showlegend=False)
                texto = "Gráfica comparativa de edades en el Cáncer Infantil"

            fig = fig1.to_html()
    except:
        div = "Su consulta no tiene casos para mostrar, realice otra consulta"

    return render(request, "cancerinfantil/graficas.html",
                {"fig": fig, "texto": texto, "republica": estados, "anio": anios, "agruedad": agruedad,
                "df": df, "div": div, "defaultEstado": defaultEstado, "tipoGrafica": tipoGrafica, "defaultTipo": defaultTipo,
                "defaultAnio": defaultAnio, "defaultRango": defaultRango})


