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
    div = ""
    if request.method == "POST":
        nombre = request.POST.get("Nombre", None)
        apellidop = request.POST.get("ApellidoP", None)
        apellidom = request.POST.get("ApellidoM", None)
        correo = request.POST.get("Correo", None)
        mensaje = request.POST.get("Mensaje", None)

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
            'apellidom': apellidom,
            'correo': correo,
            'mensaje': mensaje
        }
        send_email(context)
        div = "Su mensaje ha sido enviado"

    return render(request, "home/contacto.html", {"div": div})


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

