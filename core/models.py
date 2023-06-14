from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class TipoProducto(models.Model):
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion
    

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    precio = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=200)
    tipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True)
    fechagregado = models.DateField(null=True)
    fechamodificado = models.DateField(null=True)
    historial_compras = models.ForeignKey('Historial', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class ItemCarrito(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    foto = models.ImageField(null=True, blank=True)
    fecha_compra = models.DateTimeField(default=timezone.now)
    
class Suscripcion(models.Model):
    nombrecompleto = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.CharField(max_length=100)
    numerotelefono = models.PositiveIntegerField()
    contraseña = models.CharField(max_length=100)
    confirmarcontraseña = models.CharField(max_length=100)
    numerotarjeta = models.PositiveIntegerField()
    fechavencimiento = models.DateField()
    cvv = models.PositiveIntegerField()

    def __str__(self):
        return self.nombrecompleto
    
class Historial(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Historial #{self.id}'