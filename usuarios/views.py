from django.shortcuts import render

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
    return render(request, "usuarios.html")
