"""
URL configuration for weblacteos project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import path
from lacteos import views
from lacteos.views import *


def es_administrador(user):
    return user.groups.filter(name='Administracion').exists()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/',(views.administracion), name='home'),
    path('users/',(views.registerUser), name='users'),
    path('users/<int:id_user>/',(views.editUser), name='detalle_user'),
    path('users/<int:id_user>/eliminar',(views.deleteUser), name='eliminar_user'),
    path('cerrarsesion/',views.cerrarSesion),
    path('',views.signin, name='signin'),
    path('produccion/',views.produccion, name='produccion'),
    path('productos/',views.registerProducto, name='productos' ),
    path('product/<int:id_producto>/',views.editProducto, name='detalle_producto'),
    path('product/<int:id_producto>/eliminar',views.deleteProducto, name='eliminar_producto'),
    path('items/',views.registerItem, name='items'),
    path('provedores/',views.registerProvedor, name='provedores' ),
    path('provedor/<int:id_provedor>/',views.editProvedor, name='detalle_provedor'),
    path('provedor/<int:id_provedor>/eliminar',views.deleteProvedor, name='eliminar_provedor'),
    path('almacen/',views.registerLote, name='almacen' ),
    path('almacen/<int:id_lote>/',views.editLote, name='detalle_lote'),
    path('almacen/<int:id_lote>/eliminar',views.deleteLote, name='eliminar_lote'),
    path('register_detalle_lote/',views.registerDetalleLote, name='registre_detalle_lote' ),
    path('delete_detalle_lote/<int:id_detalle_lote>/eliminar',views.deleteDetalleLote, name='eliminar_detalle_lote'),
    path('ventas/',views.ventas, name='ventas'),
    path('registro_venta/',views.registroVenta, name='registroVenta' ),    
    path('detalle_venta/<int:id_venta>/',views.editVenta, name='detalle_venta'),
    path('eliminar_venta/<int:id_venta>/eliminar',views.deleteVenta, name='eliminar_venta'),    
    path('register_detalle_venta/',views.registerDetalleVenta, name='registre_detalle_venta' ),
    path('delete_detalle_venta/<int:id_detalle_venta>/eliminar',views.deleteDetalleVenta, name='eliminar_detalle_venta'),
    
    path('reingreso/',views.registerReingresoLote, name='reingreso_lote'),
    path('reingreso/<int:id_rein>/',views.editReingresoLote, name='detalle_reingreso'),
    path('reingreso/<int:id_rein>/eliminar',views.deleteReingresoLote, name='eliminar_reingreso'),
    path('register_detalle_reingreso_lote/',views.registerDetalleReingreso, name='registre_detalle_reingreso' ),
    path('delete_detalle_reingreso_lote/<int:id_detalle_reingreso>/eliminar',views.deleteDetalleReingreso, name='eliminar_detalle_reingreso'),


    path('merma/',views.registerMerma, name='registroMerma' ),    
    path('detalle_merma/<int:id_merma>/',views.editMerma, name='detalle_merma'),
    path('eliminar_merma/<int:id_merma>/eliminar',views.deleteMerma, name='eliminar_merma'),
    path('register_detalle_merma/',views.registerDetalleMerma, name='registre_detalle_merma' ),
    path('delete_detalle_merma/<int:id_detalle_merma>/eliminar',views.deleteDetalleMerma, name='eliminar_detalle_merma'),  
    
    path('reportes_productos/',user_passes_test(es_administrador)(views.reportesProductos), name='reportes_productos'),
    path('detalleReporteProducto/<int:id_producto>/',user_passes_test(es_administrador)(views.detallereportesProductos), name='reporte_detalle_producto'),
    path('reporteAlmacen/',views.reporteAlmacen, name='reporteAlmacen' ), 
    path('reporteVentas/',views.reporteVentas, name='reporteVentas' ), 

    path('pdf_venta/<int:id_venta>/',PdfVenta.as_view(), name='pdfVenta'),

    path('pdf_almacen/<int:id_lote>/',PdfAlmacen.as_view(), name='pdfAlmacen'),

]
