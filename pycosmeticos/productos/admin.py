from django.contrib import admin

from .models import Producto, CategoriaProducto, TipoProducto, ColorProducto, Descuento, FacturaEmitida, DetalleFacturaEmitida, CuponDescuento, Entrega, ProductoDescuento, Reseña, DescuentoPedido
from .models import Auditoria
from .models import PerfilUsuario

admin.site.register(Producto)
admin.site.register(CategoriaProducto)
admin.site.register(TipoProducto)
admin.site.register(ColorProducto)
admin.site.register(Descuento)
admin.site.register(FacturaEmitida)
admin.site.register(DetalleFacturaEmitida)
admin.site.register(CuponDescuento)
admin.site.register(Entrega)
admin.site.register(ProductoDescuento)
admin.site.register(Reseña)
admin.site.register(DescuentoPedido)
admin.site.register(Auditoria)
admin.site.register(PerfilUsuario)