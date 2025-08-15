from django.urls import path

from . import views 

app_name = 'productos'

urlpatterns = [
    path('', views.productos_lista, name='list'),
    path('<int:producto_id>/', views.producto_detalle, name='detalle'),
]