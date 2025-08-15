from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from datetime import date
from datetime import timedelta
from .models import CategoriaProducto
from .models import TipoProducto
from .models import ColorProducto
from .models import Producto
from .models import Descuento
from .models import CuponDescuento
from .models import FacturaEmitida
from .models import DetalleFacturaEmitida
from .models import Entrega
from .models import ProductoDescuento
from .models import Entrega
from .models import Reseña
from .models import DescuentoPedido
from .models import Cliente
from .models import Auditoria
from .models import PerfilUsuario

def productos_lista(request):
    categoria_id = request.GET.get('categoria') 
    productos = Producto.objects.all()
    categorias = CategoriaProducto.objects.all()
    categoria_seleccionada = None

    if categoria_id:  
        productos = productos.filter(tipo__categoria_id=categoria_id)
        categoria_seleccionada = int(categoria_id)  

    return render(request, "productos/lista.html", {
        "qry_productos_lista": productos,
        "categorias": categorias,
        "categoria_seleccionada": categoria_seleccionada
    })

def obtener_descuento(producto):
    hoy = date.today()
    descuento = Descuento.objects.filter(
        activo=True,
        fecha_inicio__lte=hoy,
        fecha_fin__gte=hoy
    ).first()
    if descuento:
        if descuento.tipo == 'porcentaje':
            precio_final = producto.precio * (1 - descuento.valor / 100)
        else:
            precio_final = producto.precio - descuento.valor
        return precio_final
    return producto.precio

def producto_detalle(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    # Precio con descuento si aplica
    precio_final = obtener_descuento(producto)
    
    # Productos similares: mismo tipo, excepto el actual
    productos_similares = Producto.objects.filter(tipo=producto.tipo).exclude(id=producto.id)[:4]
    
    # Aquí suponiendo que tu modelo Producto tiene una relación 'reseñas' (related_name='reseñas')
    reseñas = producto.reseñas.all()  # si no existe, reemplaza con el nombre correcto
    
    return render(request, 'productos/producto_detalle.html', {
        'producto': producto,
        'precio_final': precio_final,
        'productos_similares': productos_similares,
        'reseñas': reseñas
    })

def calcular_envio(factura):
    """
    Retorna el costo de envío según el total de la factura.
    Envío gratuito si factura.total >= 100, estándar 15 si es menor.
    """
    if factura.total >= 100:
        return 0
    return 15

def obtener_descuento_por_factura(total):
    descuentos = DescuentoPedido.objects.filter(activo=True, min_total__lte=total).order_by('-porcentaje')
    if descuentos.exists():
        return descuentos.first().porcentaje / 100
    return 0

def agregar_al_carrito(request, producto_id):
    cantidad = int(request.POST.get('cantidad', 1))
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        carrito[str(producto_id)] += cantidad
    else:
        carrito[str(producto_id)] = cantidad

    request.session['carrito'] = carrito
    return redirect('productos:ver_carrito')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0

    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=producto_id)
        subtotal = producto.precio * cantidad
        total += subtotal
        productos.append({
            'producto': producto,
            'cantidad': cantidad,
            'subtotal': subtotal
        })

    # Calcular descuento por pedido
    descuento_porcentaje = obtener_descuento_por_factura(total)
    total_con_descuento = total * (1 - descuento_porcentaje)

    # Calcular envío
    envio = 0 if total_con_descuento >= 100 else 15
    total_final = total_con_descuento + envio

    return render(request, 'productos/carrito.html', {
        'productos': productos,
        'total': total,
        'descuento_porcentaje': descuento_porcentaje * 100,
        'total_con_descuento': total_con_descuento,
        'envio': envio,
        'total_final': total_final
    })

def actualizar_carrito(request, producto_id):
    cantidad = int(request.POST.get('cantidad', 1))
    carrito = request.session.get('carrito', {})

    if cantidad > 0:
        carrito[str(producto_id)] = cantidad
    else:
        carrito.pop(str(producto_id), None)

    request.session['carrito'] = carrito
    return redirect('productos:ver_carrito')

