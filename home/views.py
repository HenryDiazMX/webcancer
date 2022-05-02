import time

from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import BadHeaderError
from django.shortcuts import render, HttpResponse
from django.template.loader import get_template

from home import models

# Create your views here.
from webcancer import settings


def home(request):
    return render(request, "home/index2.html")


def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre", None)
        apellidop = request.POST.get("apellidoP", None)
        apellidom = request.POST.get("apellidoM", None)
        correo = request.POST.get("correo", None)
        mensaje = request.POST.get("mensaje", None)

        models.registro.objects.create(
            nombre=nombre,
            apellidop=apellidop,
            apellidom=apellidom,
            correo=correo,
            mensaje=mensaje
        )
        context = {
            'nombre': nombre,
            'apellidop': apellidop,
            'apellidop': apellidop,
            'apellidom': apellidom,
            'correo': correo,
            'mensaje': mensaje
        }
        # send_email(context)
        time.sleep(3)
    return render(request, "home/contacto.html")


def send_email(context):
    template = get_template('home/email_content.html')
    content = template.render(context)

    email = EmailMultiAlternatives(
        'Mensaje del sitio web de Ciencia de Datos',
        'Mensaje:',
        settings.EMAIL_HOST_USER,
        ['henrydcmaster@gmail.com'],
    )

    email.attach_alternative(content, 'text/html')
    email.send()
