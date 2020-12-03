from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Rol2(models.Model):
    roles = (
        ('S', 'Secretaria'),
        ('M', 'Profesional medico'),
        ('V', 'Ventas'),
        ('T', 'Taller'),
        ('G', 'Gerencia'),
    )
    tipo = models.CharField(max_length=1, choices=roles)

    def __str__(self):
        return f" {self.tipo} "

class Clasificacion(models.Model):
    valores = (
        ('L', 'Lentes'),
        ('G', 'Gotas'),
        ('P', 'Pastillas'),
    )
    tipo = models.CharField(max_length=1, choices=valores)

    def __str__(self):
        return f" {self.tipo} "

class EstadoPedido(models.Model):
    valores = (
        ('P', 'Pendiente'),
        ('O', 'Pedido'),
        ('T', 'Taller'),
        ('F', 'Finalizado'),
    )
    tipo = models.CharField(max_length=1, choices=valores)

    def __str__(self):
        return f" {self.tipo}  {self.get_tipo_display()}"

class TipoPago(models.Model):
    valores = (
        ('T', 'Tarjeta Credito'),
        ('D', 'Debito'),
        ('V', 'Billetera Virtual'),
        ('E', 'Efectivo'),
    )
    tipo = models.CharField(max_length=1, choices=valores)

    def __str__(self):
        return f" {self.tipo} {self.get_tipo_display()}"

class Personal(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personaluser")
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.IntegerField()
    email = models.CharField(max_length=50)
    rol = models.ForeignKey(Rol2, on_delete=models.CASCADE, related_name="rolusuario")

    def __str__(self):
        return f" {self.id} : {self.nombre} {self.apellido} {self.telefono} {self.email} "


class Paciente(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.IntegerField()

    def __str__(self):
        return f" {self.id} : {self.nombre} {self.apellido} {self.telefono} "

class HistoriaClinica(models.Model):
    medico = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name="medicos")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="pacientes")
    observacion = models.CharField(max_length=255)

    def __str__(self):
        return f" {self.id} : {self.medico} {self.paciente} {self.observacion} "

class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255)
    clasificacion = models.ForeignKey(Clasificacion, on_delete=models.CASCADE, related_name="tipoproducto")
    laboratorio = models.CharField(max_length=50)
    lejos = models.BooleanField()
    izquierda = models.BooleanField()
    armazon = models.BooleanField()
    precio = models.FloatField()

    def __str__(self):
        return f" {self.id} : {self.nombre} {self.descripcion} {self.clasificacion} {self.laboratorio} {self.precio} "

class Pedido(models.Model):
    fecha = models.DateTimeField(default=datetime.now)
    vendedor = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name="vendedorx")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="pacientex")
    tipoPago = models.ForeignKey(TipoPago, on_delete=models.CASCADE, related_name="tipopagox")
    estado = models.ForeignKey(EstadoPedido, on_delete=models.CASCADE, related_name="estadox")
    def __str__(self):
        return f" {self.id} : {self.fecha} Paciente {self.paciente} Tipo de Pago: {self.tipoPago} Estado: {self.estado} "

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="pedidositem")
    fecha = models.DateTimeField(default=datetime.now)## para simplificar los reportes
    vendedor = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name="vendedorx2")## para simplificar reporte
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="pacientex2")## para simplificar reporte
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="productoitem")
    cantidad = models.IntegerField()
    total = models.FloatField()
    lejos = models.BooleanField(default=False)
    izquierda = models.BooleanField(default=False)
    armazon = models.BooleanField(default=False)

class Turno(models.Model):
    secretaria = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name="secretariaturno")
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="pacienteturno")
    medico = models.ForeignKey(Personal, on_delete=models.CASCADE, related_name="medicoturno")
    fecha = models.DateField()
    hora = models.TimeField()
    pacientepresente = models.BooleanField(default=False)
    ##form = MyForm(initial={'my_field':True})

    def __str__(self):
        return f" {self.id} : {self.fecha} {self.hora} secretaria {self.secretaria} paciente: {self.paciente} medico: {self.medico} Presente: {self.pacientepresente}"

