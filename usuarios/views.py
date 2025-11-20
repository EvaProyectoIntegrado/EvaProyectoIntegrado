from django.shortcuts import render
from api.models import Usuario 

def login_view(request):
    return render(request, "login.html")

def register_view(request):
    return render(request, "registrar.html")

def dashboard(request):
    return render(request, "dashboard.html")

def madres_view(request):
    return render(request, "madres.html")

def partos_view(request):
    return render(request, "partos.html")

def rn_view(request):
    return render(request, "rn.html")

def usuarios_view(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuarios.html", {"usuarios": usuarios})

