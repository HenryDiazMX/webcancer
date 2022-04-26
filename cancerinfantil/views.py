import csv
import pandas as pd
import folium
from pprint import pprint
import plotly.express as px
import simplekml as simplekml
import openpyxl
from django import forms
from django.shortcuts import render
from django.http import HttpResponse

from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# Generacion de la pagina de listas, llamando a los datos de la base
@csrf_exempt
def listascancer(request):
    estados = Casostotalrepublica.objects.order_by('ent_resid').all().distinct('ent_resid')
    municipios = Casostotalrepublica.objects.order_by('mun_resid').all().distinct('mun_resid')
    localidades = Casostotalrepublica.objects.order_by('loc_resid').all().distinct('loc_resid')
    años = Casostotalrepublica.objects.order_by('anio_regis').all().distinct('anio_regis')
    tipoCancer = Casostotalrepublica.objects.order_by('lista_mex').all().distinct('lista_mex')
    genero = Casostotalrepublica.objects.order_by('sexo').all().distinct('sexo')
    agruedad = Casostotalrepublica.objects.distinct('agru_edad')

    return render(request, "cancerinfantil/listas.html",
                  {"estados": estados, "municipios": municipios, "localidades": localidades, "años": años,
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


@csrf_exempt
def export_csv(request):
    global queryset, response, df
    queryset = Casostotalrepublica.objects.all()
    if request.method == 'POST':
        # query
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
        # get fields of model
        queryset = queryset.order_by('id')
        options = Casostotalrepublica._meta
        fields = [field.name for field in options.fields]
        # build response
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="ListasCancerInfantil.csv"'},
        )
        # writer
        writer = csv.writer(response)
        # writer header
        writer.writerow([options.get_field(field).verbose_name for field in fields])
        # writing data
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in fields])

    return response


# Generacion de la vista inicial de la pagina de Mapas, genera el mapa sin casos, al hacer un POST toma los datos para hacer filtros
@csrf_exempt
def mapascancer(request):
    div = ""
    estados = republicaapi.objects.distinct('ent_resid')
    municipios = republicaapi.objects.distinct('mun_resid')
    localidades = republicaapi.objects.distinct('loc_resid')
    años = republicaapi.objects.distinct('anio_regis')
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
        "republica": estados, "estado": municipios, "municipio": localidades, "año": años,
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
    datos = Casostotalrepublica.objects.all().values()
    df = pd.DataFrame(datos)
    estados = Casostotalrepublica.objects.distinct('ent_resid')
    años = Casostotalrepublica.objects.distinct('anio_regis')
    agruedad = Casostotalrepublica.objects.distinct('agru_edad')
    fig = ""
    texto = ""

    if request.method == 'POST':
        if request.POST['frmEstado'] != "TODOS":
            datos = datos.filter(ent_resid=request.POST['frmEstado'])
        if request.POST['frmAño'] != "TODOS":
            datos = datos.filter(anio_regis=request.POST['frmAño'])
        if request.POST['frmRangoEdad'] != "TODOS":
            datos = datos.filter(agru_edad=request.POST['frmRangoEdad'])

        df = pd.DataFrame(datos)

        if request.POST['frmTipo'] == "DOMINANTE":
            datos2 = pd.DataFrame()
            for i in range(0, len(df)):
                datos2.loc[i, 'año'] = df.loc[i, 'anio_regis']
                datos2.loc[i, 'lista_mex'] = df.loc[i, 'lista_mex']
            value_counts = datos2.value_counts(sort=True)
            df_val_counts = pd.DataFrame(value_counts)
            datos3 = df_val_counts.reset_index()
            datos3.columns = ['Año', 'Tipo De Cancer', 'Conteo']  # change column names
            fig1 = px.pie(datos3, values='Conteo', names='Tipo De Cancer')
            fig1.update_traces(hoverinfo='label+percent', textposition='inside')
            fig1.update_layout(autosize=True, uniformtext_minsize=16, uniformtext_mode='hide',
                               legend_itemsizing="constant")
            texto = "Grafica de los tipos de Cancer Dominantes"
        if request.POST['frmTipo'] == "GENERO":
            datos2 = pd.DataFrame()
            for i in range(0, len(df)):
                datos2.loc[i, 'AÑO'] = df.loc[i, 'anio_regis']
                datos2.loc[i, 'SEXO'] = df.loc[i, 'sexo']
            value_counts = datos2.value_counts(sort=True)
            df_val_counts = pd.DataFrame(value_counts)
            datos3 = df_val_counts.reset_index()
            datos3.columns = ['AÑO', 'SEXO', 'CONTEO']  # change column names
            fig1 = px.bar(datos3, x="AÑO", y="CONTEO", color="SEXO", height=700)
            texto = "Graficas por Año de Registro y Genero"
        if request.POST['frmTipo'] == "OCURRENCIA":
            datos2 = pd.DataFrame()
            for i in range(0, len(df)):
                datos2.loc[i, 'SITIO_OCUR'] = df.loc[i, 'sitio_ocur']
            value_counts = datos2.value_counts(sort=True)
            df_val_counts = pd.DataFrame(value_counts)
            datos3 = df_val_counts.reset_index()
            datos3.columns = ['SITIO DE OCURRENCIA', 'CONTEO']  # change column names
            fig1 = px.bar(datos3, x="SITIO DE OCURRENCIA", y="CONTEO", color='SITIO DE OCURRENCIA', text="CONTEO",
                          height=700)
            fig1.update_traces(textposition='outside')
            fig1.update_layout(uniformtext_minsize=1, uniformtext_mode='hide', showlegend=False)
            texto = "Lugares de Ocurrencia"
        if request.POST['frmTipo'] == "AREA":
            datos2 = pd.DataFrame()
            for i in range(0, len(df)):
                datos2.loc[i, 'AÑO'] = df.loc[i, 'anio_regis']
                datos2.loc[i, 'TIPO DE AREA'] = df.loc[i, 'area_ur']
            value_counts = datos2.value_counts(sort=True)
            df_val_counts = pd.DataFrame(value_counts)
            datos3 = df_val_counts.reset_index()
            datos3.columns = ['AÑO', 'TIPO DE AREA', 'CONTEO']  # change column names
            fig1 = px.bar(datos3, x="AÑO", y="CONTEO", color="TIPO DE AREA", height=700)
            texto = "Tipo de Area donde Residia el Niño(a)"
        if request.POST['frmTipo'] == "EDAD":
            datos2 = pd.DataFrame()
            for i in range(0, len(df)):
                datos2.loc[i, 'EDAD'] = df.loc[i, 'edad_abs']
            value_counts = datos2.value_counts(sort=True)
            df_val_counts = pd.DataFrame(value_counts)
            datos3 = df_val_counts.reset_index()
            datos3.columns = ['EDAD', 'CONTEO']  # change column names
            datos3 = datos3.sort_values('EDAD', ascending=True)
            fig1 = px.bar(datos3, x="EDAD", y="CONTEO", color='EDAD', text="CONTEO", height=700)
            fig1.update_traces(textposition='outside')
            fig1.update_layout(uniformtext_minsize=7, uniformtext_mode='hide', showlegend=False)
            texto = "Grafica comparativa de edades en el Cancer Infantil"

        fig = fig1.to_html()

    return render(request, "cancerinfantil/graficas.html",
                  {"fig": fig, "texto": texto, "republica": estados, "año": años, "agruedad": agruedad,
                   "df": df})
