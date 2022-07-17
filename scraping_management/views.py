from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.views import View
from django.views.generic import ListView,TemplateView
from django.views.generic.edit import CreateView
from django.forms import modelformset_factory,TextInput
from .models import Ejecucion,EjecucionParametro,SitioWeb,Spider,Parametro,Oferta
from .forms import SpiderForm
from .services import request_parameters_generator
import requests

class EjecucionListView(ListView):
    model = Ejecucion
    context_object_name = 'ejecuciones'
    paginate_by = 30
    template_name = 'scraping_management/extractores.html'

class OfertasListView(ListView):
    model = Oferta
    context_object_name = 'ofertas'
    paginate_by = 100
    template_name = 'scraping_management/ofertas.html'

    def get_queryset(self):
        sitio_web = SitioWeb.objects.get(pk=self.kwargs['pk'])
        ejecuciones = sitio_web.ejecucion_set.all()
        p = Oferta.objects.none()
        for ejecucion in ejecuciones:
            ofertas = ejecucion.oferta_set.all()
            p = p.union(p,ofertas)

        return p


class SitioWebListView(ListView):
    model = SitioWeb
    context_object_name = 'sitios_web'
    paginate_by = 20
    template_name = 'scraping_management/sitios_web.html'


class CrearEjecucionView(CreateView):
    model = Ejecucion
    fields = ['sitio_web','categoria','spider']
    template_name = 'scraping_management/create_records.html'
    success_url = '/dashboard/entry_success'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registro de Ejecucion'
        return context


class CrearSitioWebView(CreateView):
    model = SitioWeb
    fields = ['nombre','dominio','descripcion','empresa']
    template_name = 'scraping_management/create_records.html'
    success_url = '/dashboard/entry_success'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registro de Sitio Web'
        return context

class FormSuccessView(View):
    def get(self, request, *args, **kwargs):
        messages.success(request,'Registro creado correctamente')
        return render(request,'scraping_management/mensajes.html')

def GestionarEjecuciones(request):
    return render(request,'scraping_management/extractores.html')

def ejecutar(request,pk):
    ejecucion = get_object_or_404(Ejecucion,pk=pk)
    if request.method == 'GET':
        if ejecucion.parametros.all().exists() == False:
            messages.error(request, 'Antes de ejecutar primero debe ingresar los parametros')
        else:
            url = 'http://localhost:6800/schedule.json'
            data = request_parameters_generator(ejecucion,True)
            #print(data)
            response = requests.post(url, data=data)
            json_response = response.json()
            if json_response['status'] == 'ok':
                messages.success(request, f'Ejecucion exitosa,jobid:{json_response["jobid"]}')
            else:
                messages.error(request, f'Fallo en la ejecucion:{json_response["message"]}')


        return render(request,'scraping_management/mensajes.html')




def parametros_form(request,pk):
    ejecucion = get_object_or_404(Ejecucion,pk=pk)
    EjecucionParametroFormSet = modelformset_factory(EjecucionParametro,fields=('valor_parametro',),extra=0,widgets={'valor_parametro':TextInput(attrs={'size':50})})
    if ejecucion.parametros.all().exists() == False:
        parametros = ejecucion.spider.parametro_set.all()
        ejecucion.parametros.add(*parametros)

    queryset = ejecucion.ejecucionparametro_set.all()
    if request.method == 'POST':
        formset = EjecucionParametroFormSet(request.POST,queryset=queryset)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Parametros actualizados correctamente')
    else:
        formset = EjecucionParametroFormSet(queryset=queryset)

    return render(request,'scraping_management/parametros_edit.html',{'formset':formset,'id':pk})

def resultados_prueba_view(request,pk):
    ejecucion = get_object_or_404(Ejecucion, pk=pk)
    if request.method == 'GET':
        data = request_parameters_generator(ejecucion, False)
        url = 'http://localhost:9080/crawl.json?'
        response = requests.get(url, params=data)
        json_response = response.json()
        items_list=[]
        if json_response['status'] == 'ok':
            if 'errors' in json_response:
                messages.error(request, f'Fallo en la ejecucion:{json_response["message"]}')
                return render(request, 'scraping_management/resultados_prueba.html',
                              {'items': '', 'keys': '', 'items_count': 0})
            else:
                for i in range(len(json_response['items'])):
                    items_list.append(json_response['items'][i])

                item_keys = []
                items_count = json_response['stats']['item_scraped_count']
                for key in items_list[0].keys():
                    item_keys.append(key)

                return render(request, 'scraping_management/resultados_prueba.html',
                              {'items': items_list, 'keys': item_keys, 'items_count': items_count})

        else:
            messages.error(request, f'Fallo en la ejecucion:{json_response["message"]}')

    return render(request,'scraping_management/resultados_prueba.html')



def probar_parametros(request):
    if request.method == 'POST':
        ProbarParametroFormSet = modelformset_factory(EjecucionParametro, fields=('valor_parametro',), extra=0)
        if 'parametros_form' in request.POST:
            print('es parametro')
            spider_form = SpiderForm(request.POST)
            probar_parametros_form = ProbarParametroFormSet(request.POST)
            if probar_parametros_form.is_valid():
                probar_parametros_form.save()
                return redirect(f'resultados_prueba/{probar_parametros_form[0].instance.ejecucion.pk}')

        if 'spider_selected' in request.POST:
            spider_form = SpiderForm(request.POST)
            if spider_form.is_valid():
                spider = Spider.objects.get(pk=spider_form.cleaned_data['spider'].pk)
                ejecucion = Ejecucion(spider=spider)
                ejecucion.save()
                parametros = spider.parametro_set.all()
                ejecucion.parametros.add(*parametros)
                ejecucion_parametro = ejecucion.ejecucionparametro_set.all()
                probar_parametros_form = ProbarParametroFormSet(queryset=ejecucion_parametro)
                print('es spider')

    else:
        spider_form = SpiderForm()
        probar_parametros_form = None

    return render(request,'scraping_management/probar_parametros.html',{'spider_form':spider_form,'probar_parametros_form':probar_parametros_form})