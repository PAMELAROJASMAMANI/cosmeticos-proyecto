from django.db import models
from django.contrib.auth.models import User
from usuarios.models import PerfilUsuario


class CategoriaProducto(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.categoria.nombre})"


class ColorProducto(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    color = models.ForeignKey(ColorProducto, on_delete=models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)  # Aquí va la imagen
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class CuponDescuento(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=20)  # porcentaje / monto_fijo
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_expiracion = models.DateTimeField(blank=True, null=True)  # nuevo campo
    uso_maximo = models.IntegerField(default=1)
    veces_usado = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} ({self.tipo})"


class FacturaEmitida(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_emision = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    forma_pago = models.CharField(max_length=50, blank=True, null=True)
    estado_pago = models.CharField(max_length=50, default='Pendiente')
    contabilizada = models.CharField(max_length=1, default='N')
    glosa = models.CharField(max_length=200, blank=True, null=True)
    tipo_venta = models.CharField(max_length=50, default='Online')
    cupon = models.ForeignKey(CuponDescuento, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Factura {self.id} - {self.total}"


class DetalleFacturaEmitida(models.Model):
    factura = models.ForeignKey(FacturaEmitida, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Entrega(models.Model):
    factura = models.ForeignKey(FacturaEmitida, on_delete=models.CASCADE)
    empresa_envio = models.CharField(max_length=100, blank=True, null=True)
    numero_seguimiento = models.CharField(max_length=100, blank=True, null=True)
    fecha_envio = models.DateField(blank=True, null=True)
    fecha_entrega_estimada = models.DateField(blank=True, null=True)
    fecha_entregada = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=50, default='Pendiente')
    observacion = models.TextField(blank=True, null=True)


class Auditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=100)
    tabla_afectada = models.CharField(max_length=100)
    id_registro = models.IntegerField()
    fecha_hora = models.DateTimeField(auto_now_add=True)


class Descuento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=20)  # porcentaje / monto_fijo
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"


class ProductoDescuento(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    descuento = models.ForeignKey(Descuento, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('producto', 'descuento')

class DescuentoPedido(models.Model):
    nombre = models.CharField(max_length=100)
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    min_total = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.porcentaje}%)"

class Reseña(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='reseñas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    calificacion = models.PositiveSmallIntegerField(default=5)  # 1 a 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.producto.nombre} ({self.calificacion}⭐)"

    def estrellas(self):
        """Devuelve las estrellas como string para mostrar en el template"""
        return "★" * self.calificacion + "☆" * (5 - self.calificacion)
