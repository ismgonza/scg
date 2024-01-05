from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserForm
from .models import Usuario, Cuenta, Reporte

def sign_in(request):
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'user/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = UserForm(request.POST)

        if form.is_valid():
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']

            usuarios = Usuario.objects.filter(correo=correo)

            if usuarios.exists():
                usuario = usuarios.first()

                if usuario.verificar_contrasena(password):

                    if usuario.tipo == 'Admin':

                        request.session['user_correo'] = usuario.correo
                        request.session['user_tipo'] = usuario.tipo
                        request.session['user_cuenta_nombre'] = usuario.cuenta.nombre
                        cuenta_nombre = usuario.cuenta.nombre

                        return HttpResponseRedirect(reverse("index", kwargs={'nombre_cuenta': cuenta_nombre}))
                    elif usuario.tipo == 'Cliente':
                        
                        request.session['user_correo'] = usuario.correo
                        request.session['user_tipo'] = usuario.tipo
                        request.session['user_cuenta_nombre'] = usuario.cuenta.nombre
                        cuenta_nombre = usuario.cuenta.nombre

                        return HttpResponseRedirect(reverse("client", kwargs={'nombre_cuenta': cuenta_nombre}))
                            
                    else:
                        messages.error(request, 'Tipo de usuario no reconocido')
                        # Puedes ajustar la redirección en este caso según tus necesidades
                        return redirect('login')
                else:
                    messages.error(request, 'Credenciales incorrectas')
            else:
                messages.error(request, 'Usuario no encontrado')

        else:
            messages.error(request, 'Formulario no válido. Revisa los campos.')

    form = UserForm()
    return render(request, 'user/login.html', {'form': form})


def client_view(request, nombre_cuenta):
    # Recupera la información del usuario de la sesión
    user_tipo = request.session.get('user_tipo')
    user_cuenta_nombre = request.session.get('user_cuenta_nombre')

    try:
        # Buscar la cuenta en la base de datos
        cuenta = get_object_or_404(Cuenta, nombre=user_cuenta_nombre)

        # Verificar si el usuario tiene el tipo correcto y la cuenta correcta
        if user_tipo == 'Cliente' and user_cuenta_nombre == nombre_cuenta:
            # Obtener todos los informes y ordenarlos por fecha de creación
            reportes = Reporte.objects.filter(cuenta_reporte=cuenta).order_by('-fecha_reporte')

            # Configurar la paginación
            elementos_por_pagina = 10  # Ajusta según tus necesidades
            paginator = Paginator(reportes, elementos_por_pagina)
            page = request.GET.get('page')

            try:
                reportes_paginados = paginator.page(page)
            except PageNotAnInteger:
                reportes_paginados = paginator.page(1)
            except EmptyPage:
                reportes_paginados = paginator.page(paginator.num_pages)

            # Pasar los informes paginados al contexto
            context = {'nombre_cuenta': nombre_cuenta, 'reportes': reportes_paginados}
            return render(request, 'user/client.html', context)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    except Cuenta.DoesNotExist:
        messages.error(request, 'La cuenta no existe')
        return redirect('login')
    
def index_view(request, nombre_cuenta):
    # Recupera la información del usuario de la sesión
    user_tipo = request.session.get('user_tipo')
    user_cuenta_nombre = request.session.get('user_cuenta_nombre')

    try:
        # Buscar la cuenta en la base de datos
        cuenta = get_object_or_404(Cuenta, nombre=user_cuenta_nombre)

        # Verificar si el usuario tiene el tipo correcto y la cuenta correcta
        if user_tipo == 'Admin' and user_cuenta_nombre == nombre_cuenta:
            # Tu lógica de vista aquí
            return render(request, 'user/index.html', {'nombre_cuenta': nombre_cuenta})
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    except Cuenta.DoesNotExist:
        messages.error(request, 'La cuenta no existe')
        return redirect('login')