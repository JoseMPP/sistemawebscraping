from .models import Ejecucion
import json
def request_parameters_generator(ejecucion,esProduccion):
    if esProduccion:
        parametros = ejecucion.ejecucionparametro_set.all()
        data = {}
        data['project'] = 'web_service_production'
        data['spider'] = ejecucion.spider.nombre
        data['ejecucion'] = ejecucion.pk
        for argumento in parametros:
            data[argumento.parametro.nombre]  = argumento.valor_parametro
    else:
        parametros = ejecucion.ejecucionparametro_set.all()
        argumentos = {}
        for valor in parametros:
            if valor.parametro.nombre == 'url':
                url = valor.valor_parametro
            else:
                argumentos[valor.parametro.nombre] = valor.valor_parametro

        data = {
            'spider_name': ejecucion.spider.nombre,
            'url': url,
            'crawl_args': json.dumps(argumentos)
        }

    return data


