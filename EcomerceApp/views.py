from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.http import Http404
from .models import Productos, Categoria, Marca, Proveedores, Carrito, ListaDeseos, UsuarioCliente, DireccionesEnvio, Ventas,DetalleVenta
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CrearUsuario, ConfirmarUsuario, ConfirmarUsuarioCliente, UsuarioClienteForm, EditarPerflForm, DireccionesEnvioForm,VentasForm, DetalleVentaForm
from django.forms import modelformset_factory
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.db.models import Q #Para poder mostrar busquedas avanzadas, leer documentacion para mas detalles

# Create your views here.

def index (request):
    return render(request, 'Index.html')

@login_required
def perfil_usuario(request):
    if request.user.is_authenticated:
            
        usuario_cliente = request.user.usuario_cliente
    
        direcciones = usuario_cliente.direcciones.all()
        ventas = Ventas.objects.filter(id_usuario=request.user).order_by('-fecha')

        context = {
        'user': request.user,
        'usuario_cliente': usuario_cliente,
        'direcciones': direcciones,
        'ventas': ventas
        }

        return render(request, 'Perfil_Usuario.html', context)
    else:
        return redirect('Login')


@login_required
def finalizar_compra(request, id):
    usuario_cliente= get_object_or_404(UsuarioCliente, user=request.user) #Obtenemos el usuario cliente modelo UsuarioCliente
    carrito_items = Carrito.objects.filter(id_usuario=request.user) #Obtenemos los productos del carrito
    direcciones = DireccionesEnvio.objects.filter(usuario_cliente=usuario_cliente)#Obtenemos las direcciones de envio del usuarrio para opciones de envio.

    if not carrito_items.exists():#Si el carrito esta vacio, mostramos un mensaje de error.
        messages.error(request,"El carrito se encuentra vacío, Agregue productos antes de finalizar la compra")
        return redirect('ver_carrito')
    
    #Calculamos el total de la venta
    total_venta = sum(item.producto.precio * item.cantidad for item in carrito_items)
    
    
    if request.method == 'POST':#Si el metodo es POST, procedemos a guardar los datos
        direccion_id = request.POST.get('direccion')#Obtenemos el post de la DIRECCION
        if not direccion_id:#Si no es seleccionado una direccion, procedemos a mostrar un  error en pantalla
            messages.error(request,"Debe seleccionar una direccion de envio")
            return redirect('finalizar_compra', id=id)
        try:
            direccion_seleccionada= DireccionesEnvio.objects.get(id=direccion_id, usuario_cliente=usuario_cliente)#Obtenemos la direccion seleccionada

            #Creamos la venta
            venta= Ventas.objects.create(
                id_usuario = request.user,
                total_venta = 0, #Lo calculamos mas adelante
                estado ='Pendiente'
            )
            total_venta = 0
            for item in carrito_items:
                subtotal = item.producto.precio * item.cantidad
                DetalleVenta.objects.create(
                    venta=venta,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio,
                    subtotal=subtotal
                )

                total_venta += subtotal
            venta.total_venta = total_venta
            venta.estado='Pagado' #Cambiamos a Pagado antes de guardar 
            venta.save()
        
        # Procedemos a vaciar el carrito del cliente
            carrito_items.delete()

            messages.success(request,'Compra realizada con éxito!.')
            return redirect('Confirmacion_Compra', id=venta.id)
        except DireccionesEnvio.DoesNotExist:
            messages.error(request,"La dirección seleccionada no es válida")
        except Exception as e:
            messages.error(request, f"Hubo un error al procesar su compra: {str(e)}")


    return render(request, 'Finalizar_compra.html',{
        'usuario_cliente':usuario_cliente,
        'carrito_items':carrito_items,
        'direcciones':direcciones,
        'total_venta':total_venta
    })

@login_required
def confirmacion_compra(request, id):
    venta = get_object_or_404(Ventas, id=id, id_usuario = request.user)
    return render(request, "confirmacion_compra.html",{
        'venta': venta
    })

def productos(request):
    query = request.GET.get('q', '')
    if query:
        productos = Productos.objects.filter(
            Q(name__icontains=query) | #Filtra por nombre
            Q(descripcion__icontains=query) | #Filtra por descripcion
            Q(categoria__descripcion__icontains=query) | #Filtra por categoria
            Q(marca__name__icontains=query) #Filtra por marca
        )
    else:
        productos = Productos.objects.all() #Codigo ORM para mostrar todos los productos

    return render (request, 'Productos.html', {
        'productos': productos,
        'query': query #Pasamos el termino de busqueda a la plantilla para ser mostrado
    })

def detalle_producto(request, id):

    producto = get_object_or_404(Productos, id=id)
    
    productos_relacionados = Productos.objects.filter(
        categoria = producto.categoria
    ).exclude(id=producto.id)[:8]
    return render (request, 'Producto_Detalles.html',
                   {'producto': producto,
                   'productos_relacionados': productos_relacionados})


#Procedemos con la creacion de la vista para poder crear usuarios

def Crear_Usuario(request):
    if request.method == 'POST':

        form_usuario = CrearUsuario(request.POST)
        print(request.POST)#Para confirmar que datos nos da importante para confirmar los datos
        if form_usuario.is_valid():

          #vamos a validar los datos del model predeterminado de django User
            username = form_usuario.cleaned_data['username']
            email = form_usuario.cleaned_data['email']
            first_name = form_usuario.cleaned_data['nombre']
            last_name = form_usuario.cleaned_data['apellido']
            password = form_usuario.cleaned_data['password']

          #Creamos el usuario en el mdelo User

            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=make_password(password) #make_password sirve para hashear la contraseña
          )
          #Datos adicionales del modelo UsuarioCliente en este caso solo guardaremos la fecha de nacimiento, luego desde el perfil de usuario se podran cargar los demas datos
            fecha_nacimiento=  form_usuario.cleaned_data['fecha_nacimiento']
          #Los datos adicionales del modelo UsuarioCliente
            UsuarioCliente.objects.create(
                user=user,
                fecha_nacimiento=fecha_nacimiento
          )
            #redireccionamos una vez hecho al login nuevamente, podemos cambiar tambien al perfil de usuario
            return redirect('login')
    else:
        form_usuario=CrearUsuario()

    return render(request, 'Crear_Usuario_Form.html',
                  {'form_usuario':form_usuario})


#ESTA FUNCION CORRESPONDE A LA CREACION DE USUARIOCLIENTE DIFERENTE DE LA FUNCION ANTERIOR

def crear_usuario_cliente (request):

    if request.method == 'POST':
        form = UsuarioClienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente!')
            return redirect('Index.html') #debe de redireccionar a la pagina del perfil de usuario
    else:
        form = UsuarioClienteForm() 

    return render(request, 'Crear_Usuario_Form.html',{'form': form})

#Esta funcion para login_ingreso, es para validar los datos, pero ya con el model user predeterminado de Django.
def login_ingreso(request):
    if request.method == 'POST':
        formulario_login = ConfirmarUsuario(request.POST)
        if formulario_login.is_valid():
            usuario = formulario_login.cleaned_data['username']  # Username o email
            contraseña = formulario_login.cleaned_data['password']
            user = User.objects.filter(username=usuario).first()
            # Intentar autenticar directamente
            usuario = authenticate(request, usuario=user.username, password=contraseña)
            
            if usuario is not None:
                # Inicio de sesión exitoso
                login(request, usuario)
                print("Autenticación exitosa. Usuario:", usuario)
                return redirect('Index')
            else:
                # Credenciales incorrectas
                formulario_login.add_error(None, "Credenciales incorrectas. Verifica tu usuario y contraseña.")
    else:
        formulario_login = ConfirmarUsuario()

    return render(request, 'login.html', {
        'formulario_login': formulario_login
    })
#////////////////////////////////////////////////////
#Ahora procedemos a generar una vista, para poder validar el Usuario Cliente, ya con el model que generamos propio para el cliente.

def login_usuario_cliente(request):
    if request.method == 'POST':
        formulario_login_cliente = ConfirmarUsuarioCliente(request.POST)
        if formulario_login_cliente.is_valid():
            #Procedemos a recuperar los datos de nuestro Formulario ConfirmarUsuarioCliente
            usuario = formulario_login_cliente.cleaned_data.get('username')
            contraseña = formulario_login_cliente.cleaned_data.get('password')
            #Autenticamos el usuario

            usuario=authenticate(request, username=usuario, password=contraseña)

            if usuario is not None:
                #Si todo esta ok, procedemos a loguear al usuario
                login(request,usuario)
                return redirect('Index')
            else:
                #Si no existe el usuario, mostraremos el siguiente mensaje de ERROR!
                formulario_login_cliente.add_error(None, "Usuario o contraseña incorrectos")
    else:
        formulario_login_cliente=ConfirmarUsuarioCliente()
    
    return render(request, 'login.html', {
        'formulario_login_cliente': formulario_login_cliente
    })

#/////////////////////////////////////////////////


#PROCEDEMOS A CREAR LAS VISTAS PARA LISTA DE DESEOS, CARRITO y PERFIL DE USUARIO

#VISTA PARA MOSTRAR EL CARRITO/LISTA DE DESEOS, SOLO SI TENEMOS EL USUARIO VALIDADO
@login_required
def carrito(request):
    #CON OBJECTS.FILLTER LO QUE HAREMOS SERA OBTENER TODOS LOS ARTICULOS DE NUESTRO CARRITO
    carrito_item = Carrito.objects.filter(usuario=request.user)
    #VAMOS A CALCULAR EL VALOR TOTAL, PARA ELLO LO ASIGNAMOS A UNA VARIABLE item.total_producto EL CUAL LO LLEVAMOS A NUESTRA PLANTILLA
    for item in carrito_item:
        item.total_producto = float(item.producto.precio) * item.cantidad
    total = sum(float(item.total_producto) for item in carrito_item)
    #RENDERIZAMOS NUESTRA PLANTILLA DE CARRITO, CON LOS DATOS CORRESPONDIENTES
    return render (request, 'Agregar_Carrito.html', {
        'carrito_item': carrito_item,
        'total': total
    })

#FUNCIONES DE VISTAS, LAS CUALES ACCEDEMOS DESDE NUESTRO NAV CON LOS ICONOS DEL CARRITO/DESEO
@login_required
def ver_la_lista_deseos(request):
    lista_item = ListaDeseos.objects.filter(id_usuario_id=request.user)

    for item in lista_item:
        item.name=(item.producto.name)
        item.descripcion=(item.producto.descripcion)
    
    return render(request, 'Lista_de_deseos.html', {
        'lista_item':lista_item
    })

@login_required
def editar_perfil(request):
    #FORMULARIO USUARIO CLIENTE
    user = request.user
    try:
        usuario_cliente = user.usuario_cliente
    except UsuarioCliente.DoesNotExist:
        raise Http404("El perfil de Cliente no existe.")

    #FORMULARIO DIRECCIONES
    #Utilizamos Formset para las direcciones
    DirecionEnviosFormSet = modelformset_factory(
        DireccionesEnvio, #Llamamos a nuestro modelo
        form=DireccionesEnvioForm, #Generamos nuestra variable que contiene el formulario direcciones
        fields = ['direccion', 'ciudad', 'departamento', 'tipo', 'es_principal'],
        extra=1, #Para poder permitir que podamos añadir una neuva direccion
        can_delete = True #Para perminitr eliminar direcciones existentes
    )

    if request.method == 'POST':
        form_edit_perfil=EditarPerflForm(request.POST, instance=user, usuario_cliente=usuario_cliente)
        formset_direcciones = DirecionEnviosFormSet(
            request.POST, queryset=usuario_cliente.direcciones.all()
        )
        if form_edit_perfil.is_valid() and formset_direcciones.is_valid():
            #Actualizamos los datos del modelo User
            user = form_edit_perfil.save()
            #Actualizamos los datos del modelo UsuarioCliente
            usuario_cliente.telefono = form_edit_perfil.cleaned_data['telefono']
            usuario_cliente.direccion = form_edit_perfil.cleaned_data['direccion']
            usuario_cliente.fecha_nacimiento = form_edit_perfil.cleaned_data['fecha_nacimiento']
            usuario_cliente.genero = form_edit_perfil.cleaned_data['genero']
            usuario_cliente.save()

            #Guardamos/Actualizamos los datos del modelo direcciones
            direcciones = formset_direcciones.save(commit=False)
            for direccion in direcciones:
                direccion.usuario_cliente = usuario_cliente
                direccion.save()
            formset_direcciones.save()

            messages.success(request, "Tu perfil ha sido actualizado correctamente")
            return redirect('Perfil_Usuario')
    else:
        form_edit_perfil=EditarPerflForm(instance=user, usuario_cliente=usuario_cliente)
        formset_direcciones = DirecionEnviosFormSet(queryset=usuario_cliente.direcciones.all())
    return render(request, 'editar_perfil.html',
                  {'form_edit_perfil':form_edit_perfil,
                  'formset_direcciones': formset_direcciones,
                   })


#FUNCION PARA AGREGAR LOS PRODUCTOS AL CARRITO. 

@login_required
def carrito(request):
    #CON OBJECTS.FILLTER LO QUE HAREMOS SERA OBTENER TODOS LOS ARTICULOS DE NUESTRO CARRITO
    carrito_item = Carrito.objects.filter(id_usuario_id=request.user)
    #VAMOS A CALCULAR EL VALOR TOTAL, PARA ELLO LO ASIGNAMOS A UNA VARIABLE item.total_producto EL CUAL LO LLEVAMOS A NUESTRA PLANTILLA
    for item in carrito_item:
        item.total_producto = float(item.producto.precio) * item.cantidad
    total = sum(float(item.total_producto) for item in carrito_item)
    #RENDERIZAMOS NUESTRA PLANTILLA DE CARRITO, CON LOS DATOS CORRESPONDIENTES
    return render (request, 'Agregar_Carrito.html', {
        'carrito_item': carrito_item,
        'total': total
    })

@login_required
def agregar_al_carrito(request, id):

    producto = get_object_or_404(Productos, id=id)

    #Ahora verificamos si el producto ya esta en el carrito del usuario de la siguiente manera:
    cantidad = int(request.POST.get('cantidad', 1))
    
    carrito_item, created = Carrito.objects.get_or_create(id_usuario_id=request.user.id, producto=producto)

    #NUESTRA SENTENCIA IF PARA CONFIRMAR SI EL PRODUCTO YA EXISTE, DEBERA DE INCREMENTAR + 1

    if not created:
        carrito_item.cantidad += cantidad
        carrito_item.save()
    
    #PASAMOS AL ELSE SI NO ESTA EN EL CARITO, GENERAMOS CON LA CANTIDAD 1
    
    else:
        carrito_item.cantidad = cantidad
        carrito_item.save()

    #LUEGO DE ESTO PROCEDEMOS   1A REDIRECCIONAR A NUESTRA LISTA DE PRODUCTOS

    return redirect ('ver_carrito') 
    #TAMBIEN PODEMOS REDIRECCIONAR DIRECTO A NUESTRO CARRITO, PARA VER LOS PRODUCTOS, PERO EN ESTE CASO DEJAMOS QUE EL USUARIO DECIDA CUANDO IR AL CARRITO.

    #AHORA PROCEDEMOS DE LA MISMA MANERA QUE AGREGAMOS AL CARRITO, LO HAREMOS PARA AGREGAR A NUESTRA LISTA DE DESEOS, VAMOS A MOSTRAR UNA PANTALLA CON LOS PRODUCTOS SELECCIONADOS, NO HAREMOS ALGUN CALCULO, SOLO MOSTRAREMOS DICHOS PRODUCTOS



@login_required
def agregar_lista_de_deseos(request, id):
 
    producto = get_object_or_404(Productos, id=id)

    lista_item, created = ListaDeseos.objects.get_or_create(id_usuario_id=request.user.id, producto=producto)

    if not created:
        lista_item.cantidad += 1
        lista_item.save()
    
    else: 
        lista_item.cantidad = 1
        lista_item.save()
    
    return redirect('ver_lista_deseos')


#FUNCION para eliminar productos de la lista deseos

@login_required
def eliminar_lista_deseos(request,id):
    #Verificar si el item de lista de deseos existe en nuestra BSD
    lista_item = get_object_or_404(ListaDeseos, id=id, id_usuario_id=request.user.id)

    #Obtenemos el producto asociado.
    producto = lista_item.producto
    print(f"Producto encontrado correctamente:{producto.name}")#Para confirmar si efectivamente encontramos el producto

    #Procedemos a eliminar el producto de nuestra lista de deseos
    lista_item.delete()
    print(f"Producto{producto.name} eliminado correctamente")#Confirmamos que el producto fue eliminado correctamente
    return redirect('ver_lista_deseos')

#FUNCIONES PARA ELIMINAR PRODUCTOS DEL CARRITO

#REDUCIR LA CANTIDAD
@login_required
def eliminar_del_carrito(request, id):
    try:
        carrito_item = Carrito.objects.get(id=id, id_usuario_id=request.user.id)
        
        
        #Condicion para disminuir el producto y no eliminarlo

        if carrito_item.cantidad > 1:

            carrito_item.cantidad -= 1
            carrito_item.save()
        
        else:
            # Si la cantidad es 1 o mayor, procedemos a eliminarlo
            carrito_item.delete()
            messages.success(request, 'Producto eliminado del carrito correctamente')
    except Carrito.DoesNotExist:
        messages.error(request,'El producto no se encontró en tu carrito')
    return redirect('ver_carrito')

#ELIMINAR EL PRODUCTO
@login_required
def eliminar_carrito(request, id):

    carrito_item=get_object_or_404(Carrito, id=id, id_usuario_id=request.user)

    if carrito_item:
        carrito_item.delete()
    
    return redirect('ver_carrito')