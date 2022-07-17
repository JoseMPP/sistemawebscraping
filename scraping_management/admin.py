from django.contrib import admin
from scraping_management import models
# Register your models here.
admin.site.register(models.SitioWeb)
admin.site.register(models.Spider)
admin.site.register(models.Parametro)
admin.site.register(models.Categoria)
admin.site.register(models.Caracteristica)
admin.site.register(models.Ejecucion)
admin.site.register(models.EjecucionParametro)
admin.site.register(models.Oferta)