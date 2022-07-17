from django.urls import path
from . import views,api_views
app_name = 'scraping_management'
urlpatterns = [
    path('',views.GestionarEjecuciones,name='dashboard'),
    #path('api/all_ofertas/',api_views.all_ofertas,name='all_ofertas'),
    path('api/all_ofertas/',api_views.AllOfertas.as_view(),name='all_ofertas'),
    path('api/first_oferta_api',api_views.first_oferta_api),
    path('probar_parametros/resultados_prueba/<int:pk>',views.resultados_prueba_view,name='resultados_prueba'),
    path('ejecuciones/',views.EjecucionListView.as_view(),name='ejecuciones_list'),
    path('sitios_web/',views.SitioWebListView.as_view(),name='sitios_web_list'),
    path('ofertas_list/<int:pk>',views.OfertasListView.as_view(),name='ofertas_list'),
    path('parametros_edit/<int:pk>',views.parametros_form,name='ejecucion_parametro_edit'),
    path('ejecutar/<int:pk>',views.ejecutar,name='ejecutar'),
    path('crear_ejecucion/',views.CrearEjecucionView.as_view(),name='crear_ejecucion'),
    path('crear_sitio_web/',views.CrearSitioWebView.as_view(),name='crear_sitio_web'),
    path('entry_success',views.FormSuccessView.as_view(),name='entry_success'),
    path('probar_parametros/',views.probar_parametros,name='probar_parametros'),

]