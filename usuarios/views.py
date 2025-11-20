from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegistroForm
from .models import Perfil


def registro(request):
    """Vista para registrar un nuevo usuario y asignarle un rol."""
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            # No guardamos aún para poder asignar la contraseña manualmente
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Encriptamos la contraseña
            user.save()

            # Asignamos el rol al perfil relacionado
            user.perfil.rol = form.cleaned_data['rol']
            user.perfil.save()

            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('usuarios:login')
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


def login_view(request):
    """Vista para iniciar sesión de usuario."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect('peliculas:lista_pelicula')  # Corregido
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    return render(request, 'usuarios/login.html')


@login_required
def logout_view(request):
    """Vista para cerrar sesión."""
    logout(request)
    return redirect('usuarios:login')