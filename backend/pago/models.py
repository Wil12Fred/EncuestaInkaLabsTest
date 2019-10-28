from django.db import models

class Entidad(models.Model):
    nombre = models.CharField(max_length=30)
    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    def __str__(self):
        return self.entidad.nombre + ": " + self.nombre


class ReturnSuministro(models.Model):
    monto = models.CharField(max_length=30, null=True, blank=True)
    descripcion = models.CharField(max_length=30, null=True, blank=True)
    titular = models.CharField(max_length=30)
    codigo = models.IntegerField()

class Suministro(models.Model):
    codigo = models.IntegerField()
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    titular = models.CharField(max_length=30)
    monto = models.IntegerField(default=0)
    #returnMonto = models.CharField(max_length=30, null=True, blank = True)
    #returnDescription = models.CharField(max_length=30, null=True, blank = True)
    def __str__(self):
        return str(self.servicio)+": " + str(codigo)

class Tarjeta(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Pago(models.Model):
    #tarjeta = models.CharField( max_length=16)
    #tarjeta_debito = models.BooleanField( default=False)
    #tipo_tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, blank=True, null=True);
    #vencimiento = MyModel
    #vencimiento = YearMonthField() #models.DateField(null=True)
    vencimiento = models.DateField(null=True)
    #cvv = models.CharField( max_length=3, null = True )
    #monto = models.IntegerField()
    #operacion = models.ForeignKey(Suministro, on_delete=models.CASCADE)
    #entidad = models.CharField( max_length=30)
    #validado = models.BooleanField(default=False)

class Pago2(models.Model):
    tarjeta = models.CharField( max_length=16)
    #tarjeta_debito = models.BooleanField( default=False)
    #tipo_tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, blank=True, null=True);
    #vencimiento = MyModel
    #vencimiento = YearMonthField() #models.DateField(null=True)
    vencimiento = models.DateField(null=True)
    cvv = models.CharField( max_length=3, null = True )
    #monto = models.IntegerField()
    operacion = models.ForeignKey(Suministro, on_delete=models.CASCADE)
    #entidad = models.CharField( max_length=30)
    #validado = models.BooleanField(default=False)

class PagoD(models.Model):
    tarjeta = models.CharField( max_length=16)
    #tarjeta_debito = models.BooleanField( default=False)
    #tipo_tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, blank=True, null=True);
    #vencimiento = MyModel
    #vencimiento = YearMonthField() #models.DateField(null=True)
    vencimiento = models.DateField(null=True)
    cvv = models.CharField( max_length=3, null = True )
    #monto = models.IntegerField()
    #operacion = models.ForeignKey(Suministro, on_delete=models.CASCADE)
    operacion = models.IntegerField()
    #entidad = models.CharField( max_length=30)
    #validado = models.BooleanField(default=False)
# Create your models here.
