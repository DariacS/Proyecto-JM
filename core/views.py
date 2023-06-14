from django.shortcuts import render,redirect,get_object_or_404
from django.db.models import Sum, F , Q
from django.contrib import messages
from .models import *
from .forms import *
from .carrito import *
from django.contrib.auth.decorators import login_required
import requests

# Create your views here.
def index(request):
    return render(request,'core/index.html')
@login_required
def indexapi(request):
        respuesta = requests.get('http://127.0.0.1:8000/api/productos/')
        respuesta2 = requests.get('https://mindicador.cl/api/')

        productos = respuesta.json()
        monedas = respuesta2.json()

        data = {'listado':productos,
                'monedas':monedas,}
        return render(request,'core/indexapi.html',data)

@login_required
def perfil(request):
        return render(request,'core/perfil.html')

@login_required
def seguimiento(request):
    return render(request,'core/seguimiento.html')

@login_required
def suscribete(request):
    return render(request,'core/suscribete.html')

@login_required
def subscrito(request):
    return render(request,'core/subscrito.html')

@login_required
def historial(request):
    # Obtén los productos del historial que han sido comprados
    productos_historial = Producto.objects.filter(historial_compras__usuario=request.user)

    # Pasa los productos a la plantilla
    context = {'productos': productos_historial}
    return render(request, 'core/historial.html', context)

def guardar_en_historial(request):
    items_carrito = ItemCarrito.objects.filter(usuario=request.user)

    for item in items_carrito:
        historial1 = Historial(usuario=request.user, producto=item.producto, cantidad=item.cantidad)
        historial1.save()

    # No es necesario eliminar los elementos del carrito, ya que se han movido al historial
    items_carrito.update(usuario=None)

    return redirect('historial')



@login_required
def carrito(request):
    respuesta = requests.get('https://mindicador.cl/api/dolar').json()
    valor_usd = respuesta['serie'][0]['valor']

    items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    cantidad_total = items_carrito.aggregate(total_cantidad=Sum('cantidad'))
    cantidad_seleccionada = request.GET.get('cantidad')
    
    
    precio_total = items_carrito.annotate(precio_total=F('producto__precio') * F('cantidad')).aggregate(total_precio=Sum('precio_total'))
    if precio_total['total_precio'] is not None and valor_usd != 0:
        precio_total = round(precio_total['total_precio'] / valor_usd,2)
    else:
        precio_total = 0
    
    return render(request, 'core/carrito.html', {
        'items_carrito': items_carrito,
        'cantidad_total': cantidad_total['total_cantidad'],
        'precio_total': precio_total,
        'cantidad_seleccionada': cantidad_seleccionada,
    })
    
@login_required
def comprar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    
    if producto.stock > 0:
        producto.stock -= 1
        producto.save()
        guardar_en_historial(request)
        
    return redirect("carrito")    

@login_required
def devolvercarrito(request):
    items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    
    # Devolver la cantidad de productos al stock disponible
    for item in items_carrito:
        Producto.objects.filter(id=item.producto.id).update(stock=F('stock') + item.cantidad)
    
    # Eliminar todos los productos del carrito
    items_carrito.delete()
    
    return redirect('carrito')


@login_required
def agregaralcarrito(request, id):
    producto = Producto.objects.get(id=id)
    
    # Verificar si el stock es cero
    if producto.stock == 0:
        messages.error(request, 'Hay un producto agotado en tu carrito.')
    else:
        item_carrito, created = ItemCarrito.objects.get_or_create(
            producto=producto,
            usuario=request.user,
            defaults={'cantidad': 1}
        )
        if not created:
            item_carrito.cantidad += 1
            item_carrito.save()
        
        # Restar la cantidad del producto al stock disponible
        Producto.objects.filter(id=id).update(stock=F('stock') - 1)
        
    total_precio = ItemCarrito.objects.filter(usuario=request.user).aggregate(Sum('producto__precio'))
    request.session['total_precio'] = total_precio.get('producto__precio__sum', 0)
    
    return redirect('carrito')

@login_required
def eliminar_producto(request, id):
    producto = Producto.objects.get(id=id)
    ItemCarrito.objects.filter(producto=producto, usuario=request.user).delete()
    return redirect("carrito")

@login_required
def restar_producto(request, id):
    item_carrito = ItemCarrito.objects.get(producto__id=id, usuario=request.user)
    
    if item_carrito.cantidad > 1:
        item_carrito.cantidad -= 1
        Producto.objects.filter(id=item_carrito.producto.id).update(stock=F('stock') + 1)
        item_carrito.save()
    else:
        # Devolver la cantidad del producto al stock disponible
        Producto.objects.filter(id=item_carrito.producto.id).update(stock=F('stock') + 1)
        item_carrito.delete()

    return redirect("carrito")

@login_required
def limpiar_carrito(request):
    ItemCarrito.objects.filter(usuario=request.user).delete()
    request.session['total_precio'] = 0
    return redirect("carrito")

@login_required
def eliminarcarrito(request, id):
    carrito = Carrito(request)
    producto = Producto.objects.get(id=id)
    carrito.restar(producto)
    return redirect("carrito")

@login_required
def productos(request):
    productosALL = Producto.objects.all()
    datos = {
        'listaProductos': productosALL
    }
    
    return render(request, 'core/productos.html', datos)

@login_required
def suscriptores(request):
    suscriptoresALL = Suscripcion.objects.all()
    datos = {
        'listasuscriptores' : suscriptoresALL
    }
    if not request.user.is_superuser:
    
        return redirect('index')
    else:
        return render(request,'core/suscriptores.html',datos)

@login_required
def agregarsus(request):
    datos= {
        'form' : SusForm()
    }
    if request.method == 'POST':
        formulario = SusForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = "Suscriptor Guardado Correctamente"
            
    return render(request,'core/suscribete.html',datos)

@login_required
def modificarsus(request, id):
    Suscriptor = Suscripcion.objects.get(id=id)
    datos= {
        'form' : SusForm(instance=Suscriptor)
    }
    
    if request.method == 'POST':
        formulario = SusForm(data=request.POST,instance=Suscriptor, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = "Producto Modificado Correctamente"
            datos['form'] = formulario
    return render(request,'core/modificarsus.html', datos)

@login_required
def eliminarsus(request, id):
    Suscriptor = Suscripcion.objects.get(id=id); # OBTENEMOS UN PRODUCTO
    Suscriptor.delete()

    return redirect(to='suscriptores')

@login_required
def crud(request):
    productosALL = Producto.objects.all()
    datos = {
        'listaProductos' : productosALL
    }
    if not request.user.is_superuser:
    
        return redirect('index')
    else:
        return render(request,'core/crud.html',datos)

@login_required
def agregar(request):
    datos= {
        'form' : ProductoForm()
    }
    if request.method == 'POST':
        formulario = ProductoForm(request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = "Producto Guardado Correctamente"
            
    return render(request,'core/agregar.html',datos)

@login_required
def modificar(request, id):
    productos = Producto.objects.get(id=id)
    datos= {
        'form' : ProductoForm(instance=productos)
    }
    
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST,instance=productos, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            datos['mensaje'] = "Producto Modificado Correctamente"
            datos['form'] = formulario
    return render(request,'core/modificar.html', datos)

@login_required
def eliminarproducto(request, id):
    producto = Producto.objects.get(id=id); # OBTENEMOS UN PRODUCTO
    producto.delete()

    return redirect(to="crud")
