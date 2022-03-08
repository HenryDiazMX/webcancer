"""webcancer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views as home_views
from cancerinfantil import views as cancer_views

urlpatterns = [
    path('', home_views.home, name="home"),
    path('CancerInfantil/Listas', cancer_views.listascancer, name="listascancer"),
    path('CancerInfantil/Mapas', cancer_views.mapascancer, name="mapascancer"),
    path('CancerInfantil/Graficas', cancer_views.graficascancer, name="graficascancer"),
    path('admin/', admin.site.urls),
    path('CancerInfantil/Listas/Generate', cancer_views.export_csv, name="generarlista"),
    path('CancerInfantil/Mapas/Generate', cancer_views.generarkml, name="generarKML"),
    path('CancerInfantil/Municipio', cancer_views.municipio, name="muncipio"),
    path('CancerInfantil/Localidad', cancer_views.localidad, name="localidad")
]