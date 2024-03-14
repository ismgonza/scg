import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .models import generate_reset_token
from django.contrib.auth.hashers import make_password, check_password
from .forms import UserForm, CuentaForm, ReporteForm, UsuarioForm, UsuarioFormEdit, CambiarClaveForm, TareaForm, CustomPasswordResetForm, ContratoForm
from .models import Usuario, Cuenta, Reporte, Tarea, Contrato

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

                if check_password(password, usuario.password):  # Verifica la contraseña cifrada:

                    if usuario.tipo == 'Admin':

                        request.session['user_correo'] = usuario.correo
                        request.session['user_tipo'] = usuario.tipo
                        request.session['user_cuenta_nombre'] = usuario.cuenta.nombre
                        request.session['user_tel'] = usuario.telefono
                        request.session['user_nombre'] = usuario.nombre
                        cuenta_nombre = usuario.cuenta.nombre

                        return HttpResponseRedirect(reverse("index", kwargs={'nombre_cuenta': cuenta_nombre}))
                    elif usuario.tipo == 'Cliente':
                        
                        request.session['user_correo'] = usuario.correo
                        request.session['user_tipo'] = usuario.tipo
                        request.session['user_cuenta_nombre'] = usuario.cuenta.nombre
                        request.session['user_tel'] = usuario.telefono
                        request.session['user_nombre'] = usuario.nombre
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

def sign_out(request):
    # Elimina las variables de sesión relevantes
    del request.session['user_correo']
    del request.session['user_tipo']
    del request.session['user_cuenta_nombre']
    del request.session['user_tel']
    del request.session['user_nombre']

    # Redirige a la página de inicio de sesión u otra página deseada
    return redirect('login')

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
            tareas = Tarea.objects.filter(cuenta_tarea=cuenta)

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
            context = {'nombre_cuenta': nombre_cuenta,
                        'reportes': reportes_paginados,
                        'tareas': tareas
                        }
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
    registro_exitoso = request.session.pop('registro_exitoso', False)
    registro_editado = request.session.pop('registro_editado', False)
    registro_eliminado = request.session.pop('registro_eliminado', False)

    try:
        # Buscar la cuenta en la base de datos
        cuenta = get_object_or_404(Cuenta, nombre=user_cuenta_nombre)

        # Verificar si el usuario tiene el tipo correcto y la cuenta correcta
        if user_tipo == 'Admin' and user_cuenta_nombre == nombre_cuenta:
            # Tu lógica de vista aquí
            usuarios = Usuario.objects.all()
            cuentas = Cuenta.objects.all()
            reportes = Reporte.objects.all()
            tareas = Tarea.objects.all()
            contratos = Contrato.objects.all()
            tipos = Usuario.OPCIONES_TIPO

            # Pasa los datos al contexto de la plantilla
            context = {
                'nombre_cuenta': nombre_cuenta,
                'usuarios': usuarios,
                'cuentas': cuentas,
                'reportes': reportes,
                'tareas': tareas,
                'contratos': contratos,
                'tipos': tipos,
                'registro_exitoso': registro_exitoso,
                'registro_editado': registro_editado,
                'registro_eliminado': registro_eliminado
            }

            return render(request, 'user/admin_costumers.html', context)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    except Cuenta.DoesNotExist:
        messages.error(request, 'La cuenta no existe')
        return redirect('login')
    
def view_reporte(request, id_reporte, nombre_cuenta):

    user_cuenta_nombre = request.session.get('user_cuenta_nombre')

    # Obtén el objeto Reporte específico utilizando el id_reporte y nombre_cuenta
    reporte = get_object_or_404(Reporte, id_reporte=id_reporte, cuenta_reporte__nombre=nombre_cuenta)

    # Verifica que el usuario tenga acceso a la cuenta asociada al informe
    if user_cuenta_nombre != reporte.cuenta_reporte.nombre:  # Asumiendo que tienes una relación ForeignKey entre Cuenta y Usuario en tu modelo
        return HttpResponseForbidden("No tienes permisos para ver este informe.")

    # Construye la ruta del archivo HTML basándote en el nombre de cuenta y el id_reporte
    filename = f"uploads/nessus/{id_reporte}_{nombre_cuenta.lower()}.html"

    try:
        # Abre y lee el contenido del archivo HTML
        with open(filename, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Renderiza la plantilla con el contenido del archivo HTML
        rendered_html = render_to_string('user/view_reporte.html', {'nombre_cuenta': nombre_cuenta, 'reporte': reporte, 'html_content': html_content})

        # Devuelve la respuesta HTTP con el HTML renderizado
        return HttpResponse(rendered_html)

    except FileNotFoundError:
        print(f"Archivo no encontrado: {filename}")
        return HttpResponse("El informe no está disponible.")

    except IOError as e:
        print(f"Error al leer el archivo: {e}")
        return HttpResponse("Error al leer el informe.")
    
def download_report(request, id_reporte, nombre_cuenta):
    # Construye la ruta del archivo HTML basándote en el nombre de cuenta y el id_reporte
    filename = f"uploads/dradis/{id_reporte}_{nombre_cuenta.lower()}.docx"

    try:
        # Abre y lee el contenido del archivo DOCX
        with open(filename, 'rb') as docx_file:
            # Devuelve el contenido como una respuesta para la descarga
            response = HttpResponse(docx_file.read(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename="{id_reporte}_{nombre_cuenta.lower()}.docx"'

        return response

    except FileNotFoundError:
        return HttpResponse("El informe no está disponible.")

    except IOError as e:
        return HttpResponse("Error al leer el informe.")
    
def crear_reporte(request, nombre_cuenta):
    if request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index', nombre_cuenta=nombre_cuenta)  # Cambia 'index' por el nombre de la vista a la que quieras redirigir después de guardar el reporte
    else:
        form = ReporteForm()

    return redirect('index', nombre_cuenta=nombre_cuenta)

def crear_cuenta(request, nombre_cuenta):
    if request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['registro_exitoso'] = True
            return redirect('index', nombre_cuenta=nombre_cuenta)
    else:
        form = CuentaForm()

    return redirect('index', nombre_cuenta=nombre_cuenta)

def crear_usuario(request, nombre_cuenta):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            # Generar una contraseña aleatoria usando parte del nombre y un número
            nombre = form.cleaned_data['nombre']
            parte_nombre = ''.join(random.choices(nombre.lower(), k=3))  # Usar los primeros 3 caracteres del nombre
            numero = random.randint(100, 999)  # Generar un número aleatorio de tres dígitos
            password = f"{parte_nombre}{numero}"
            hashed_password = make_password(password)
            
            # Guardar el usuario en la base de datos con la contraseña generada
            usuario = form.save(commit=False)
            usuario.password = hashed_password

            # Asignar el estado del usuario como "Enabled"
            usuario.status = 'Enabled'

            usuario.save()

            # Aquí puedes agregar cualquier lógica adicional, como redireccionar a otra página
            return redirect('index', nombre_cuenta=nombre_cuenta)
    else:
        form = UsuarioForm()
    return redirect('index', nombre_cuenta=nombre_cuenta)

def crear_tarea(request, nombre_cuenta):
    if request.method == 'GET':
        form = TareaForm()
        return render(request, 'user/crear_tarea.html', {'form': form, 'nombre_cuenta': nombre_cuenta})
    elif request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['registro_exitoso'] = True
            return redirect('index', nombre_cuenta=nombre_cuenta)
            # Lógica adicional después de guardar el reporte
    else:
        form = TareaForm()

    return redirect('index', nombre_cuenta=nombre_cuenta)

def crear_contrato(request, nombre_cuenta):
    if request.method == 'POST':
        form = ContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)  # Obtener el objeto Contrato sin guardarlo en la base de datos aún
            contrato.status = 'Active'  # Asignar el estado "Active"
            contrato.save()  # Guardar el contrato en la base de datos
            # Resto de tu lógica después de guardar el contrato
            return redirect('index', nombre_cuenta=nombre_cuenta)  # Redirige a alguna página después de la creación exitosa
    else:
        form = ContratoForm()

    return redirect('index', nombre_cuenta=nombre_cuenta)

def view_perfil(request, nombre_cuenta):
    user_cuenta_nombre = request.session.get('user_cuenta_nombre', '')
    user_correo = request.session.get('user_correo', '')
    user_tipo = request.session.get('user_tipo', '')
    user_tel = request.session.get('user_tel', '')
    user_nombre = request.session.get('user_nombre', '')

    # Puedes agregar más datos según sea necesario

    return render(request, 'user/view_perfil.html', {
        'nombre_cuenta': nombre_cuenta,
        'user_cuenta_nombre': user_cuenta_nombre,
        'user_correo': user_correo,
        'user_tipo': user_tipo,
        'user_tel': user_tel,
        'user_nombre': user_nombre
    })

def view_reset_correo(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['email']
            # Verificar si el correo existe en la base de datos
            if Usuario.objects.filter(correo=correo).exists():
                # Generar el token y enviar el correo
                form.save(request=request)

                # Recuperar la instancia de usuario
                usuario = Usuario.objects.get(correo=correo)

                # Obtener la información necesaria para construir la URL de reset_confirm
                uidb64 = urlsafe_base64_encode(force_bytes(usuario.pk))
                token = generate_reset_token(usuario)

                # Construir la URL de reset_confirm
                reset_confirm_url = reverse('reset_confirm', kwargs={
                    'uidb64': uidb64,
                    'token': token,
                })

                reset_confirm_full_url = request.build_absolute_uri(reset_confirm_url)

                # Enviar correo electrónico con el enlace para restablecer la contraseña
                subject = 'Restablecer Contraseña'
                message = f'Por favor, sigue este enlace para restablecer tu contraseña: {reset_confirm_full_url}'
                from_email = 'tu_correo@gmail.com'  # Reemplaza con tu dirección de correo de Gmail
                recipient_list = [correo]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

                request.session['reset_correo'] = correo
                
                return redirect('reset_sent')
            else:
                messages.error(request, 'El correo proporcionado no existe en nuestra base de datos.')
    else:
        form = CustomPasswordResetForm()
    return render(request, 'user/reset_correo.html', {'form': form})

def client_reports_view(request, nombre_cuenta):
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
            return render(request, 'user/client_reports.html', context)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    except Cuenta.DoesNotExist:
        messages.error(request, 'La cuenta no existe')
        return redirect('login')
    
def client_tasks_view(request, nombre_cuenta):

    user_tipo = request.session.get('user_tipo')
    user_cuenta_nombre = request.session.get('user_cuenta_nombre')

    try:
        # Buscar la cuenta en la base de datos
        cuenta = get_object_or_404(Cuenta, nombre=user_cuenta_nombre)

        # Verificar si el usuario tiene el tipo correcto y la cuenta correcta
        if user_tipo == 'Cliente' and user_cuenta_nombre == nombre_cuenta:
            
            tareas = Tarea.objects.filter(cuenta_tarea=cuenta)
            tareas_completadas = Tarea.objects.filter(cuenta_tarea=cuenta, status='Completed')

            # Pasar los informes paginados al contexto
            context = {'nombre_cuenta': nombre_cuenta,
                        'tareas': tareas,
                        'tareas_completadas': tareas_completadas
                        }
            return render(request, 'user/client_tasks.html', context)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    except Cuenta.DoesNotExist:
        messages.error(request, 'La cuenta no existe')
        return redirect('login')

def editar_cuenta(request, nombre_cuenta, id_cuenta):
    cuenta = get_object_or_404(Cuenta, id=id_cuenta)
    if request.method == 'POST':
        form = CuentaForm(request.POST, instance=cuenta)
        if form.is_valid():
            form.save()
            request.session['registro_editado'] = True
            return redirect('index', nombre_cuenta=nombre_cuenta)  # Cambia 'nombre_de_tu_vista' con el nombre de tu vista principal
    else:
        form = CuentaForm(instance=cuenta)
    return render(request, 'user/editar_cuenta.html', {'form': form, 'cuenta': cuenta, 'nombre_cuenta': nombre_cuenta})

def eliminar_cuenta(request, nombre_cuenta, id_cuenta):
    cuenta = get_object_or_404(Cuenta, id=id_cuenta)
    cuenta.delete()
    request.session['registro_eliminado'] = True
    return redirect('index', nombre_cuenta=nombre_cuenta)  # Cambia 'nombre_de_tu_vista' con el nombre de tu vista principal

def editar_reporte(request, nombre_cuenta, id_reporte):
    reporte = get_object_or_404(Reporte, id=id_reporte)
    if request.method == 'POST':
        form = ReporteForm(request.POST, instance=reporte)
        if form.is_valid():
            form.save()
            request.session['registro_editado'] = True
            return redirect('index', nombre_cuenta=nombre_cuenta)  # Cambia 'nombre_de_tu_vista' con el nombre de tu vista principal
    else:
        form = ReporteForm(instance=reporte)
    return render(request, 'user/editar_reporte.html', {'form': form, 'reporte': reporte, 'nombre_cuenta': nombre_cuenta})

def eliminar_reporte(request, nombre_cuenta, id_reporte):
    reporte = get_object_or_404(Reporte, id=id_reporte)
    reporte.delete()
    request.session['registro_eliminado'] = True
    return redirect('index', nombre_cuenta=nombre_cuenta)  # Cambia 'nombre_de_tu_vista' con el nombre de tu vista principal

def editar_usuario(request, nombre_cuenta, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    if request.method == 'POST':
        form = UsuarioFormEdit(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            request.session['registro_editado'] = True
            return redirect('index', nombre_cuenta=nombre_cuenta)  # Cambia 'nombre_de_tu_vista' con el nombre de tu vista principal
    else:
        form = UsuarioFormEdit(instance=usuario)
    return render(request, 'user/editar_usuario.html', {'form': form, 'usuario': usuario, 'nombre_cuenta': nombre_cuenta})

def eliminar_usuario(request, nombre_cuenta, id_usuario):
    usuario = get_object_or_404(Usuario, id=id_usuario)
    usuario.delete()
    request.session['registro_eliminado'] = True
    return redirect('index', nombre_cuenta=nombre_cuenta)  # Cambia 'nombre_de_tu_vista' con el nombre de tu vista principal

def editar_tarea(request, nombre_cuenta, id_tarea):
    tarea = get_object_or_404(Tarea, id=id_tarea)
    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            request.session['registro_editado'] = True
            return redirect('index', nombre_cuenta=nombre_cuenta)  # Cambia 'nombre_de_tu_vista' con el nombre de tu vista principal
    else:
        form = TareaForm(instance=tarea)
    return render(request, 'user/editar_tarea.html', {'form': form, 'tarea': tarea, 'nombre_cuenta': nombre_cuenta})

def eliminar_tarea(request, nombre_cuenta, id_tarea):
    tarea = get_object_or_404(Tarea, id=id_tarea)
    tarea.delete()
    request.session['registro_eliminado'] = True
    return redirect('index', nombre_cuenta=nombre_cuenta)  # Cambia 'nombre_de_tu_vista' con el nombre de tu vista principal

def confirmar_clave_view(request, uidb64, token):
    # Recupera el correo de la sesión
    correo = request.session.get('reset_correo', None)

    if not correo:
        # Manejar el caso en el que el correo no esté en la sesión (por seguridad)
        messages.error(request, 'Solicitud no válida para restablecer la contraseña.')
        return redirect('reset_password')
    
    if request.method == 'POST':
        form = CambiarClaveForm(request.POST)
        if form.is_valid():
            nueva_contraseña = form.cleaned_data['nueva_contraseña']
            
            usuario = Usuario.objects.get(correo=correo)

            # Cambia la contraseña del usuario usando set_password
            usuario.set_password(nueva_contraseña)
            usuario.save()

            del request.session['reset_correo']
        
            return redirect('reset_complete')  # Puedes redirigir a donde quieras
    else:
        form = CambiarClaveForm()
    return render(request, 'user/reset_clave.html', {'form': form})

def contar_tareas_por_estado():
    counts = {}
    for choice in Tarea.OPCIONES_STATUS:
        counts[choice[1]] = Tarea.objects.filter(status=choice[0]).count()
    return counts

def view_admin_tasks(request, nombre_cuenta):
    # Recupera la información del usuario de la sesión
    user_tipo = request.session.get('user_tipo')
    user_cuenta_nombre = request.session.get('user_cuenta_nombre')

    try:
        # Buscar la cuenta en la base de datos
        cuenta = get_object_or_404(Cuenta, nombre=user_cuenta_nombre)

        # Verificar si el usuario tiene el tipo correcto y la cuenta correcta
        if user_tipo == 'Admin' and user_cuenta_nombre == nombre_cuenta:
            # Tu lógica de vista aquí
            counts = contar_tareas_por_estado()
            tareas = Tarea.objects.all()
            cuentas = Cuenta.objects.all()
            opciones_status = Tarea.OPCIONES_STATUS
            opciones_sev = Tarea.OPCIONES_SEV

            # Pasa los datos al contexto de la plantilla
            context = {
                'nombre_cuenta': nombre_cuenta,
                'tareas': tareas,
                'counts': counts,
                'opciones_status': opciones_status,
                'opciones_sev': opciones_sev,
                'cuentas': cuentas
            }

            return render(request, 'user/admin_tasks.html', context)
        else:
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
    
    except Cuenta.DoesNotExist:
        messages.error(request, 'La cuenta no existe')
        return redirect('login')
    
def get_account_data(request, nombre_cuenta):
    if request.method == 'GET':
        account_name = request.GET.get('account_name')  # Obtener el nombre de la cuenta del parámetro GET
        account = Cuenta.objects.get(nombre=account_name)  # Obtener la cuenta según el nombre
        # Suponiendo que tienes los campos account_id, account_name, contract y status en tu modelo Account
        data = {
            'id_cuenta': account.id_cuenta,
            'nombre': account.nombre,
        }
        return JsonResponse(data)  # Devolver los datos como una respuesta JSON
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def view_tarea(request, nombre_cuenta, id_tarea):
    tarea = get_object_or_404(Tarea, id_tarea=id_tarea, cuenta_tarea__nombre=nombre_cuenta)
    return render(request, 'user/view_task.html', {'nombre_cuenta': nombre_cuenta, 'tarea': tarea})
