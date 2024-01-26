from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from .forms import UserForm, CuentaForm, ReporteForm, UsuarioForm, UsuarioFormEdit
from .models import Usuario, Cuenta, Reporte

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'user/reset_clave.html'  # Personaliza la plantilla según tus necesidades

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

def sign_out(request):
    # Elimina las variables de sesión relevantes
    del request.session['user_correo']
    del request.session['user_tipo']
    del request.session['user_cuenta_nombre']

    # Redirige a la página de inicio de sesión u otra página deseada
    return redirect('login')

def generate_line_chart():
    # Tu lógica para obtener los datos del gráfico aquí
    x_values = [1, 2, 3, 4, 5]
    y_values = [10, 20, 15, 25, 30]

    # Crea el gráfico
    plt.plot(x_values, y_values)
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.title('Gráfico Lineal')

    # Guarda el gráfico en un BytesIO para convertirlo a base64
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convierte el gráfico a formato base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64

def grafico_circular():
    labels = ['Manzanas', 'Plátanos', 'Uvas', 'Naranjas']
    sizes = [30, 25, 20, 25]

    # Colores para cada porción
    colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen']

    # Destacar una porción (opcional)
    explode = (0.1, 0, 0, 0)

    # Crear el gráfico de pizza
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

    # Añadir un título
    plt.title('Distribución de Frutas')

    # Guarda el gráfico en un BytesIO para convertirlo a base64
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Convierte el gráfico a formato base64
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64

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

            chart_data = generate_line_chart()

            # Pasar los informes paginados al contexto
            context = {'nombre_cuenta': nombre_cuenta,
                        'reportes': reportes_paginados,
                        'chart_data': chart_data}
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

            # Pasa los datos al contexto de la plantilla
            context = {
                'nombre_cuenta': nombre_cuenta,
                'usuarios': usuarios,
                'cuentas': cuentas,
                'reportes': reportes,
                'registro_exitoso': registro_exitoso,
                'registro_editado': registro_editado,
                'registro_eliminado': registro_eliminado
            }

            return render(request, 'user/index.html', context)
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
    if request.method == 'GET':
        form = ReporteForm()
        return render(request, 'user/crear_reporte.html', {'form': form, 'nombre_cuenta': nombre_cuenta})
    elif request.method == 'POST':
        form = ReporteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session['registro_exitoso'] = True
            return redirect('index', nombre_cuenta=nombre_cuenta)
            # Lógica adicional después de guardar el reporte
    else:
        form = ReporteForm()

    return render(request, 'crear_reporte', {'form': form, 'nombre_cuenta': nombre_cuenta})

def crear_cuenta(request, nombre_cuenta):
    if request.method == 'GET':
        form = CuentaForm()
        return render(request, 'user/crear_cuenta.html', {'form': form, 'nombre_cuenta': nombre_cuenta})
    elif request.method == 'POST':
        form = CuentaForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['registro_exitoso'] = True
            return redirect('index', nombre_cuenta=nombre_cuenta)
            # Lógica adicional después de guardar el reporte
    else:
        form = CuentaForm()

    return render(request, 'crear_cuenta', {'form': form, 'nombre_cuenta': nombre_cuenta})

def crear_usuario(request, nombre_cuenta):
    if request.method == 'GET':
        form = UsuarioForm()
        return render(request, 'user/crear_usuario.html', {'form': form, 'nombre_cuenta': nombre_cuenta})
    elif request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            request.session['registro_exitoso'] = True
            return redirect('index', nombre_cuenta=nombre_cuenta)
            # Lógica adicional después de guardar el reporte
    else:
        form = UsuarioForm()

    return render(request, 'crear_usuario', {'form': form, 'nombre_cuenta': nombre_cuenta})

def view_perfil(request, nombre_cuenta):
    user_cuenta_nombre = request.session.get('user_cuenta_nombre', '')
    user_correo = request.session.get('user_correo', '')
    user_tipo = request.session.get('user_tipo', '')

    # Puedes agregar más datos según sea necesario

    return render(request, 'user/view_perfil.html', {
        'nombre_cuenta': nombre_cuenta,
        'user_cuenta_nombre': user_cuenta_nombre,
        'user_correo': user_correo,
        'user_tipo': user_tipo,
    })

def view_reset_correo(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['email']
            # Verificar si el correo existe en la base de datos
            if Usuario.objects.filter(correo=correo).exists():
                # Generar el token y enviar el correo
                form.save(request=request)

                # Enviar correo electrónico con el enlace para restablecer la contraseña
                subject = 'Restablecer Contraseña'
                message = 'Por favor, sigue este enlace para restablecer tu contraseña.'
                from_email = 'juandiego@securitygroupcr.com'  # Reemplaza con tu dirección de correo electrónico
                recipient_list = [correo]

                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
                
                messages.success(request, 'Se ha enviado un correo con instrucciones para cambiar la contraseña.')
                return redirect('reset_sent')
            else:
                messages.error(request, 'El correo proporcionado no existe en nuestra base de datos.')
    else:
        form = PasswordResetForm()
    return render(request, 'user/reset_correo.html', {'form': form})

def view_reset_clave(request):
    return render(request, 'user/reset_clave.html')

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
    graf_circular = grafico_circular()
    context = {'nombre_cuenta': nombre_cuenta,
               'graf_circular': graf_circular}
    return render(request, 'user/client_tasks.html', context)

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