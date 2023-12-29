from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import UserForm
from .models import Usuario, Cuenta

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
                        return redirect('index')
                    elif usuario.tipo == 'Cliente':
                        # Verificar el campo 'cuenta'
                        cuenta_nombre = usuario.cuenta.nombre

                        try:
                            # Buscar la cuenta en la base de datos
                            cuenta = get_object_or_404(Cuenta, nombre=cuenta_nombre)

                            # Realizar la redirección con el nombre de la cuenta
                            return HttpResponseRedirect(reverse("client", kwargs={'nombre_cuenta': cuenta_nombre}))

                        except Cuenta.DoesNotExist:
                            messages.error(request, 'La cuenta no existe')
                            return redirect('login')
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
