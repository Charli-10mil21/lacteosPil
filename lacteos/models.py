from django.db import models
from django.contrib.auth.models import User

# from django.contrib.auth.models import AbstractUser

# Create your models here.
class Cargo(models.Model):
    nombre= models.TextField(blank=True)
    area = models.TextField(blank=True)

    def __str__(self):
        return self.nombre



class Item(models.Model):
    nombre= models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre= models.TextField(blank=True)
    u_medida = models.CharField(max_length=30)
    peso = models.PositiveIntegerField()
    precio_unidad= models.DecimalField(max_digits=10, decimal_places=2)
    id_item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    total_unidades = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    celular = models.IntegerField(blank=True)
    direccion = models.TextField()
    profesion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Lote(models.Model):
    n_lote = models.CharField(max_length=20)
    fecha = models.DateField()
    fecha_vencimiento = models.DateField(null=True)
    id_proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.n_lote

class Detalle_lote(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    id_lote = models.ForeignKey(Lote, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.IntegerField(blank=True)

    def __str__(self):
        return self.cantidad



class Estado_venta(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre_cliente = models.CharField(max_length=100)
    nit = models.IntegerField(blank=True)
    fecha = models.DateField()
    tipo_venta = models.CharField(max_length=100)
    id_estado = models.ForeignKey(Estado_venta, on_delete=models.SET_NULL, null=True, blank=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True )

    def __str__(self):
        return self.nombre_cliente

class Detalle_venta(models.Model):
     id_producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
     id_venta = models.ForeignKey(Venta, on_delete=models.SET_NULL, null=True, blank=True)
     cantidad = models.IntegerField(blank=True)
     total = models.DecimalField(max_digits=10, decimal_places=2 , null=True)

     def __str__(self):
        return self.cantidad

class Nota_venta(models.Model):
    detalle = models.CharField(max_length=100)
    id_venta = models.ForeignKey(Venta, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.detalle
    

class Reingreso_lote(models.Model):
    fecha = models.DateField()
    detalle = models.CharField(max_length=500)
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.fecha

class Detalle_reingreso(models.Model):
    id_producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
    id_reingreso_lote = models.ForeignKey(Reingreso_lote, on_delete=models.SET_NULL, null=True, blank=True)
    cantidad = models.IntegerField(blank=True,null=True,)

    def __str__(self):
        return self.cantidad

class Merma(models.Model):
    fecha = models.DateField()
    descripcion = models.CharField(max_length=500)
    id_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_merma = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.fecha

class Detalle_merma(models.Model):
     id_producto = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True, blank=True)
     id_merma = models.ForeignKey(Merma, on_delete=models.SET_NULL, null=True, blank=True)
     cantidad = models.IntegerField(blank=True)
     total = models.DecimalField(max_digits=10, decimal_places=2, null=True)

     def __str__(self):
        return self.cantidad


    