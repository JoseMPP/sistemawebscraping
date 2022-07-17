from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=70)

    class Meta:
        db_table = 'categoria'

    def __str__(self):
        return self.nombre

class Caracteristica(models.Model):
    nombre = models.CharField(max_length=30)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    class Meta:
        db_table = 'caracteristica'
    def __str__(self):
        return self.nombre

class Spider(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=70)
    es_produccion = models.BooleanField()
    class Meta:
        db_table = 'spider'
    def __str__(self):
        return self.nombre

class Parametro(models.Model):
    nombre = models.CharField(max_length=15)
    descripcion = models.CharField(max_length=70)
    spider = models.ForeignKey(Spider,on_delete=models.CASCADE)
    class Meta:
        db_table = 'parametro'
    def __str__(self):
        return self.nombre


class SitioWeb(models.Model):
    """El sitio web de donde se extraen los datos"""
    dominio = models.URLField(max_length=50)
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=70)
    empresa = models.CharField(max_length=50)
    habilitado = models.BooleanField(default=True)

    class Meta:
        db_table = 'sitiweb'
    def __str__(self):
        return self.nombre

class SitioWebParametro(models.Model):
    sitio_web = models.ForeignKey(SitioWeb,on_delete=models.CASCADE)
    parametro = models.ForeignKey(Parametro,on_delete=models.CASCADE)
    valor_parametro = models.CharField(max_length=150)

    class Meta:
        db_table = 'ejecucionparametro'
    def __str__(self):
        return  f'{self.ejecucion} {self.parametro} {self.valor_parametro}'

class Ejecucion(models.Model):
    sitio_web = models.ForeignKey(SitioWeb,null=True,on_delete=models.SET_NULL)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE,null=True)
    spider = models.ForeignKey(Spider,on_delete=models.CASCADE)
    parametros = models.ManyToManyField('Parametro',through='EjecucionParametro')

    class Meta:
        db_table = 'ejecucion'
    def __str__(self):
        return f'{self.sitio_web} {self.categoria}'

class EjecucionParametro(models.Model):
    ejecucion = models.ForeignKey(Ejecucion,on_delete=models.CASCADE)
    parametro = models.ForeignKey(Parametro,on_delete=models.CASCADE)
    valor_parametro = models.CharField(max_length=100)

    def __str__(self):
        return  f'{self.ejecucion} {self.parametro} {self.valor_parametro}'

class Oferta(models.Model):
    titulo = models.CharField(max_length=250)
    precio = models.FloatField()
    divisa =models.CharField(max_length=10)
    fecha_extraccion = models.DateTimeField()
    ejecucion = models.ForeignKey(Ejecucion,null=True,on_delete=models.SET_NULL)
    url_image = models.CharField(max_length=1000)

    class Meta:
        db_table = 'oferta'

    def __str__(self):
        return f'{self.fecha_extraccion,self.titulo}'




