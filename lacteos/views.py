from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User , Group
from .models import Producto
from .models import Item
from .models import Proveedor
from .models import Lote
from .models import Detalle_lote
from .models import Estado_venta
from .models import Venta
from .models import Detalle_venta
from .models import Reingreso_lote
from .models import Detalle_reingreso
from .models import Merma
from .models import Detalle_merma
from .forms import ProductoForm
from .forms import ProvedorForm
from .forms import LoteForm
from .forms import VentaForm
from .forms import UserForm
from .forms import ReingresoLoteForm
from .forms import MermaForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.db.models import Sum

from django.conf import settings
from django.http import HttpResponse
from xhtml2pdf import pisa
import os

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from django.views import View

from django.utils.timezone import datetime
from django.db.models import Count


# Create your views here.

# login logout
def cerrarSesion(request):
    logout(request)
    return redirect('signin')

def signin(request):
    if request.method == 'GET': 
        return render(request, 'login.html')
    else: 
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request,user)
            if user.groups.filter(name='Administracion').exists():
                return redirect('home')
            elif user.groups.filter(name='Produccion').exists():
                return redirect('produccion')
            elif user.groups.filter(name='Ventas').exists():
                return redirect('ventas')
        else:
            return render(request, 'login.html',{
                    'error' : 'el usuario o la contraseña es incorrecta'
                })


@login_required
def administracion(request):
    user = request.user
    grupos_usuario = user.groups.all().values_list('name', flat=True)
    return render(request, 'administracion.html',{
        'grupos_usuario': grupos_usuario
    })

#crud User


def registerUser(request):
    if request.method == 'GET':
        user = request.user
        grupos_usuario = user.groups.all().values_list('name', flat=True)
        usuarios = User.objects.all()
        grupos = Group.objects.all()
        return render(request, 'registroUsers.html',{
        'users': usuarios,
        'grupos': grupos,
        'grupos_usuario': grupos_usuario,
        'message': '',
        'error': ''
        })
    else: 
        if request.POST['password1'] == request.POST['password2']:
            try: 
                user = User.objects.create_user(username=request.POST['username'], first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],password=request.POST['password1'])
                # Obtener el grupo seleccionado por el usuario
                grupo_id = request.POST.get('group')
                if grupo_id:
                    group = Group.objects.get(id=grupo_id)
                    user.groups.add(group)

                user.save()
                usuarios = User.objects.all()
                return render(request, 'registroUsers.html', {
                    'form' : UserCreationForm,
                    'message' : 'el usuario fue creado correctamente',
                    'users': usuarios
                })
            except:
                usuarios = User.objects.all()
                return render(request, 'registroUsers.html', {
                    'form' : UserCreationForm,
                    'error' : 'el usuario ya existe',
                    'users': usuarios
                })
                
        else:
            usuarios = User.objects.all()
            return render(request, 'registroUsers.html',{
                    'form' : UserCreationForm,
                    'error' : 'las contraseñas no coinciden',
                    'users': usuarios
                })

@login_required
def editUser(request,id_user):
    grupos = Group.objects.all()
    user = request.user
    grupos_usuario = user.groups.all().values_list('name', flat=True)
    if request.method == 'GET':
        user = get_object_or_404(User,pk=id_user)
        
        return render(request, 'detalle_user.html',{
            'user': user,
            'grupos': grupos,
            'grupos_usuario': grupos_usuario
        })
    else:
        user = get_object_or_404(User, pk=id_user)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            # Actualiza el grupo del usuario
            grupo_id = request.POST.get('id_groups')
            grupo = get_object_or_404(Group, pk=grupo_id)
            user.groups.clear()  # Elimina todos los grupos actuales del usuario
            user.groups.add(grupo)  # Agrega el nuevo grupo seleccionado
            form.save()
            return redirect('users')
        else:
            # Si el formulario no es válido, maneja el error de alguna manera
            # Por ejemplo, muestra un mensaje de error o vuelve a renderizar el formulario
            return render(request, 'detalle_user.html', {'form': form})

@login_required
def deleteUser(request,id_user):
    user = get_object_or_404(User,pk=id_user)
    usuarios = User.objects.all().order_by('id')
    if request.method == 'POST':
        user.delete()
        return render(request, 'productos.html', {
                'message' : 'el usuario fue Eliminado correctamente',
                'users': usuarios,
            })




@login_required
def produccion(request):
    user = request.user
    grupos_usuario = user.groups.all().values_list('name', flat=True)
    return render(request, 'produccion.html',{
        'grupos_usuario': grupos_usuario
    })

# crud Producto 

@login_required
def registerProducto(request):
    if request.method == 'GET':
        user = request.user
        grupos_usuario = user.groups.all().values_list('name', flat=True)
        productos = Producto.objects.all().order_by('id')
        items = Item.objects.all()
        return render(request, 'productos.html',{
        'products': productos,
        'items': items,
        'grupos_usuario': grupos_usuario,
        'message': '',
        'error': ''
        })
    else: 
        try: 
            producto = Producto.objects.create(nombre=request.POST['nombre'], u_medida=request.POST['u_medida'], peso=request.POST['peso'], precio_unidad=request.POST['precio_unidad'],id_item_id=request.POST['item_id'])
            producto.save()
            productos = Producto.objects.all().order_by('id')
            items = Item.objects.all()
            return render(request, 'productos.html', {
                'message' : 'el producto fue creado correctamente',
                'products': productos,
                'items': items,
            })
        except:
            productos = Producto.objects.all().order_by('id')
            items = Item.objects.all()
            return render(request, 'registroUsers.html', {
                'error' : 'el producto ya existe',
                'products': productos,
                'items': items
            })

@login_required
def editProducto(request,id_producto):
    if request.method == 'GET':
        producto = get_object_or_404(Producto,pk=id_producto)
        items = Item.objects.all()
        det_lotes = Detalle_lote.objects.filter(id_producto_id=id_producto).order_by('id')
        lote = Lote.objects.all()
        cantidad_total = Detalle_lote.objects.filter(id_producto_id=id_producto).aggregate(Sum('cantidad'))['cantidad__sum']
        return render(request, 'detalle_producto.html',{
            'product': producto,
            'items' : items,
            'det_lotes' : det_lotes,
            'lote': lote,
            'cantidad_total': cantidad_total
        })
    else:
        producto = get_object_or_404(Producto,pk=id_producto)
        form = ProductoForm(request.POST, instance=producto)
        form.save()
        return redirect('productos')

@login_required
def deleteProducto(request,id_producto):
    producto = get_object_or_404(Producto,pk=id_producto)
    productos = Producto.objects.all().order_by('id')
    items = Item.objects.all()
    if request.method == 'POST':
        producto.delete()
        return render(request, 'productos.html', {
                'message' : 'el producto fue Eliminado correctamente',
                'products': productos,
                'items': items,
            })


# crud Item
@login_required
def registerItem(request):
    if request.method == 'POST':
        item = Item.objects.create(nombre=request.POST['nombre'])
        item.save()
        productos = Producto.objects.all()
        items = Item.objects.all()
        return render(request, 'productos.html', {
            'message' : 'el item fue creado correctamente',
            'products': productos,
            'items': items,
        })


#crud Proveedor
@login_required
def registerProvedor(request):
    if request.method == 'GET':
        user = request.user
        grupos_usuario = user.groups.all().values_list('name', flat=True)
        provedores = Proveedor.objects.all().order_by('id')
        return render(request, 'provedores.html',{
        'provedores': provedores,
        'grupos_usuario': grupos_usuario,
        'message': '',
        'error': ''
        })
    else: 
        try: 
            provedores = Proveedor.objects.create(nombre=request.POST['nombre'], celular=request.POST['celular'], direccion=request.POST['direccion'], profesion=request.POST['profesion'])
            provedores.save()
            provedores = Proveedor.objects.all().order_by('id')
            return render(request, 'provedores.html', {
                'message' : 'el provedor fue creado correctamente',
                'provedores': provedores,
            })
        except:
            provedores = Proveedor.objects.all().order_by('id')
            return render(request, 'provedores.html', {
                'error' : 'el producto ya existe',
                'provedores': provedores,
            })

@login_required
def editProvedor(request,id_provedor):
    if request.method == 'GET':
        user = request.user
        grupos_usuario = user.groups.all().values_list('name', flat=True)
        provedor = get_object_or_404(Proveedor,pk=id_provedor)
        return render(request, 'detalle_provedor.html',{
            'provedor': provedor,
            'grupos_usuario': grupos_usuario
        })
    else:
        provedor = get_object_or_404(Proveedor,pk=id_provedor)
        form = ProvedorForm(request.POST, instance=provedor)
        form.save()
        return redirect('provedores')

@login_required
def deleteProvedor(request,id_provedor):
    provedor = get_object_or_404(Proveedor,pk=id_provedor)
    provedores = Proveedor.objects.all().order_by('id')
    if request.method == 'POST':
        provedor.delete()
        return render(request, 'provedores.html', {
                'message' : 'el Proveedor fue Eliminado correctamente',
                'provedores': provedores,
            })


#crud Lote
@login_required
def registerLote(request):
    if request.method == 'GET':
        user = request.user
        grupos_usuario = user.groups.all().values_list('name', flat=True)
        lotes = Lote.objects.all().order_by('id')
        provedores = Proveedor.objects.all()
        users = User.objects.all()
        return render(request, 'almacen.html',{
        'lotes': lotes,
        'provedores': provedores,
        'grupos_usuario': grupos_usuario,
        'users': users,
        'message': '',
        'error': ''
        })
    else: 
        try: 
            lote = Lote.objects.create(n_lote=request.POST['n_lote'], fecha=request.POST['fecha'], fecha_vencimiento=request.POST['fecha_vencimiento'], id_user_id=request.POST['id_user'], id_proveedor_id=request.POST['id_proveedor'])
            lote.save()
            id_lote = lote.id
            lotes = Lote.objects.all().order_by('id')
            return redirect('detalle_lote',id_lote)
            # return render(request, 'almacen.html', {
            #     'message' : 'el lote fue creado correctamente',
            #     'lotes': lotes,
            # })
        except:
            lotes = Lote.objects.all().order_by('id')
            return render(request, 'almacen.html', {
                'error' : 'el lote ya existe',
                'lotes': lotes,
            })

@login_required
def editLote(request,id_lote):
    if request.method == 'GET':
        user = request.user
        grupos_usuario = user.groups.all().values_list('name', flat=True)
        lote = get_object_or_404(Lote,pk=id_lote)
        proveedores = Proveedor.objects.all()
        productos = Producto.objects.all().order_by('id')
        detLotes = Detalle_lote.objects.filter(id_lote_id =id_lote ).order_by('id')
        lotes = Lote.objects.all()
        return render(request, 'detalle_lote.html',{
            'lote': lote,
            'provedores': proveedores,
            'productos' : productos,
            'detLotes' : detLotes,
            'lotes' : lotes,
            'grupos_usuario': grupos_usuario

        })
    else:
        lote = get_object_or_404(Lote,pk=id_lote)
        form = LoteForm(request.POST, instance=lote)
        form.save()
        return redirect('almacen')

@login_required
def deleteLote(request,id_lote):
    lote = get_object_or_404(Lote,pk=id_lote)
    lotes = Lote.objects.all().order_by('id')
    if request.method == 'POST':
        lote.delete()
        return render(request, 'almacen.html', {
                'message' : 'el lote fue Eliminado correctamente',
                'lotes': lotes,
            })

#crud Detalle Lote
@login_required
def registerDetalleLote(request):
    if request.method == 'POST':
        try: 
            id_lote = request.POST['id_lote']
            
            detLote = Detalle_lote.objects.create(cantidad=request.POST['cantidad'], id_lote_id=request.POST['id_lote'], id_producto_id=request.POST['id_producto'])
            detLote.save()
            cantidad = int(request.POST['cantidad']) 
            producto = get_object_or_404(Producto, pk=request.POST['id_producto'])
            producto.total_unidades = (producto.total_unidades or 0) + cantidad
            producto.save(update_fields=['total_unidades'])
            return redirect('detalle_lote',id_lote)
        except:
            lotes = Lote.objects.all().order_by('id')
            return render(request, 'almacen.html', {
                'error' : 'el detalle no se pudo crear',
                'lotes': lotes,
            })

@login_required
def deleteDetalleLote(request,id_detalle_lote):
    detallelote = get_object_or_404(Detalle_lote,pk=id_detalle_lote)
    cantidad = int(detallelote.cantidad) 
    producto = get_object_or_404(Producto, pk=detallelote.id_producto_id)
    producto.total_unidades = (producto.total_unidades or 0) - cantidad
    producto.save(update_fields=['total_unidades'])
    id_lote = detallelote.id_lote_id
    if request.method == 'POST':
        detallelote.delete()
        return redirect('detalle_lote',id_lote)

@login_required
def ventas(request):
    user = request.user
    grupos_usuario = user.groups.all().values_list('name', flat=True)
    ventas = Venta.objects.all().order_by('id')
    estados = Estado_venta.objects.all()
    return render(request, 'ventas.html',{
        'estados': estados,
        'ventas' : ventas,
        'grupos_usuario': grupos_usuario,
        'estados': estados,
        'message': '',
        'error': ''
        })

#crud Venta

@login_required
def registroVenta(request):
    if request.method == 'POST':
        try: 
            venta = Venta.objects.create(nombre_cliente=request.POST['nombre_cliente'],nit=request.POST['nit'], fecha=request.POST['fecha'], tipo_venta=request.POST['tipo_venta'], id_estado_id=request.POST['id_estado'], id_user_id=request.POST['id_user'])
            venta.save()
            id_venta = venta.id
            return redirect('detalle_venta',id_venta)
            # return render(request, 'almacen.html', {
            #     'message' : 'el lote fue creado correctamente',
            #     'lotes': lotes,
            # })
        except:
            estados = Estado_venta.objects.all()
    return render(request, 'ventas.html',{
        'estados': estados,
        'message': '',
        'error': 'la venta no se pudo registrar'
        })

@login_required
def editVenta(request,id_venta):
    if request.method == 'GET':
        venta = get_object_or_404(Venta,pk=id_venta)
        productos = Producto.objects.all().order_by('id')
        estados = Estado_venta.objects.all()
        detventa = Detalle_venta.objects.filter(id_venta_id =id_venta ).order_by('id')
        return render(request, 'detalle_venta.html',{
            'venta': venta,
            'productos' : productos,
            'estados' : estados,
            'detventa' : detventa,

        })
    else:
       
        venta = get_object_or_404(Venta,pk=id_venta)
        form = VentaForm(request.POST, instance=venta)
        form.save()
        return redirect('ventas')
            
    
    

@login_required
def deleteVenta(request,id_venta):
    venta = get_object_or_404(Venta,pk=id_venta)
    ventas = Venta.objects.all().order_by('id')
    if request.method == 'POST':
        venta.delete()
        return render(request, 'ventas.html', {
                'message' : 'la venta fue Eliminado correctamente',
                'ventas': ventas,
            })

#crud Detalle VEnta
@login_required
def registerDetalleVenta(request):
    if request.method == 'POST':
        producto = Producto.objects.get(id=request.POST.get('id_producto'))
        precio = producto.precio_unidad
        cantidad_venta = int(request.POST.get('cantidad'))
        cantidad_producto = producto.total_unidades
        total_pagar = precio * cantidad_venta
        # try: 
        id_venta = request.POST['id_venta']
        if int(request.POST.get('cantidad')) > cantidad_producto :

            return redirect('detalle_venta',id_venta)
        else:
            detVenta = Detalle_venta.objects.create(cantidad=request.POST['cantidad'], total=total_pagar, id_producto_id=request.POST['id_producto'], id_venta_id=request.POST['id_venta'])
            detVenta.save()
            venta = get_object_or_404(Venta, pk=request.POST['id_venta'])
            venta.total_venta = (venta.total_venta or 0) + total_pagar
            venta.save(update_fields=['total_venta'])
            cantidad = int(request.POST['cantidad']) 
            producto = get_object_or_404(Producto, pk=request.POST['id_producto'])
            producto.total_unidades = (producto.total_unidades or 0) - cantidad
            producto.save(update_fields=['total_unidades'])
            return redirect('detalle_venta',id_venta)
        # except:
        #     ventas = Venta.objects.all().order_by('id')
        #     estados = Estado_venta.objects.all()
        #     return render(request, 'ventas.html', {
        #         'error' : 'no se registro la venta',
        #         'estados': estados,
        #         'ventas' : ventas,
        #     })


@login_required
def deleteDetalleVenta(request,id_detalle_venta):
    detalleVenta = get_object_or_404(Detalle_venta,pk=id_detalle_venta)
    total_pagar = detalleVenta.total
    
    id_venta = detalleVenta.id_venta_id
    if request.method == 'POST':
        venta = get_object_or_404(Venta, pk=id_venta)
        venta.total_venta = (venta.total_venta or 0) - total_pagar
        venta.save(update_fields=['total_venta'])
        cantidad = int(detalleVenta.cantidad) 
        producto = get_object_or_404(Producto, pk=detalleVenta.id_producto_id)
        producto.total_unidades = (producto.total_unidades or 0) + cantidad
        producto.save(update_fields=['total_unidades'])
        detalleVenta.delete()
        return redirect('detalle_venta',id_venta)


#crud Reingreso
@login_required
def registerReingresoLote(request):
    if request.method == 'GET':
        reingresos = Reingreso_lote.objects.all().order_by('id')
        users = User.objects.all()
        return render(request, 'reingreso_lote.html',{
        'reingresos': reingresos,
        'users': users,
        'message': '',
        'error': ''
        })
    else: 
        try: 
            reingreso = Reingreso_lote.objects.create( fecha=request.POST['fecha'], detalle=request.POST['detalle'], id_user_id=request.POST['id_user'])
            reingreso.save()
            id_rein = reingreso.id
            return redirect('detalle_reingreso',id_rein)
            # return render(request, 'almacen.html', {
            #     'message' : 'el lote fue creado correctamente',
            #     'lotes': lotes,
            # })
        except:
            reingresos = Reingreso_lote.objects.all().order_by('id')
            return render(request, 'reingreso_lote.html', {
                'error' : 'el reingreso ya existe',
                'reingresos': reingresos,
            })

@login_required
def editReingresoLote(request,id_rein):
    if request.method == 'GET':
        rein = get_object_or_404(Reingreso_lote,pk=id_rein)
        productos = Producto.objects.all().order_by('id')
        detReins = Detalle_reingreso.objects.filter(id_reingreso_lote_id =id_rein ).order_by('id')
        return render(request, 'detalle_reingreso.html',{
            'rein': rein,
            'productos' : productos,
            'detReins' : detReins,

        })
    else:
        rein = get_object_or_404(Reingreso_lote,pk=id_rein)
        form = ReingresoLoteForm(request.POST, instance=rein)
        form.save()
        return redirect('reingreso_lote')

@login_required
def deleteReingresoLote(request,id_rein):
    rein = get_object_or_404(Lote,pk=id_rein)
    reingresos = Reingreso_lote.objects.all().order_by('id')
    if request.method == 'POST':
        rein.delete()
        return render(request, 'reingreso_lote.html', {
                'message' : 'el lote fue Eliminado correctamente',
                'reingresos': reingresos,
            })


#crud Detalle Reingreso
@login_required
def registerDetalleReingreso(request):
    if request.method == 'POST':
        try: 
            id_rein = request.POST['id_rein']
            
            detReinLote = Detalle_reingreso.objects.create(cantidad=request.POST['cantidad'], id_reingreso_lote_id=request.POST['id_rein'], id_producto_id=request.POST['id_producto'])
            detReinLote.save()
            cantidad = int(request.POST['cantidad']) 
            producto = get_object_or_404(Producto, pk=request.POST['id_producto'])
            producto.total_unidades = (producto.total_unidades or 0) + cantidad
            producto.save(update_fields=['total_unidades'])
            return redirect('detalle_reingreso',id_rein)
        except:
            reingresos = Reingreso_lote.objects.all().order_by('id')
            return render(request, 'reingreso_lote.html', {
                'error' : 'el detalle no se pudo crear',
                'reingresos': reingresos,
            })

@login_required
def deleteDetalleReingreso(request,id_detalle_reingreso):
    detalleloteReingreso = get_object_or_404(Detalle_lote,pk=id_detalle_reingreso)
    id_lote = detalleloteReingreso.id_lote_id
    if request.method == 'POST':
        cantidad = int(detalleloteReingreso.cantidad) 
        producto = get_object_or_404(Producto, pk=detalleloteReingreso.id_producto_id)
        producto.total_unidades = (producto.total_unidades or 0) - cantidad
        producto.save(update_fields=['total_unidades'])
        detalleloteReingreso.delete()
        return redirect('detalle_lote',id_lote)


#crud Mermas
@login_required
def registerMerma(request):
    if request.method == 'GET':
        mermas = Merma.objects.all().order_by('id')
        users = User.objects.all()
        return render(request, 'merma.html',{
        'mermas': mermas,
        'users': users,
        'message': '',
        'error': ''
        })
    else: 
        try: 
            merma = Merma.objects.create( fecha=request.POST['fecha'], descripcion=request.POST['descripcion'], id_user_id=request.POST['id_user'])
            merma.save()
            id_merma = merma.id
            return redirect('detalle_merma',id_merma)
        except:
            mermas = Merma.objects.all().order_by('id')
            return render(request, 'merma.html', {
                'error' : 'el registro ya existe',
                'mermas': mermas,
            })

@login_required
def editMerma(request,id_merma):
    if request.method == 'GET':
        merma = get_object_or_404(Merma,pk=id_merma)
        productos = Producto.objects.all().order_by('id')
        detMermas = Detalle_merma.objects.filter(id_merma_id =id_merma ).order_by('id')
        return render(request, 'detalle_merma.html',{
            'merma': merma,
            'productos' : productos,
            'detMermas' : detMermas,

        })
    else:
        merma = get_object_or_404(Merma,pk=id_merma)
        form = MermaForm(request.POST, instance=merma)
        form.save()
        return redirect('merma')

@login_required
def deleteMerma(request,id_merma):
    merma = get_object_or_404(Lote,pk=id_merma)
    mermas = Merma.objects.all().order_by('id')
    if request.method == 'POST':
        merma.delete()
        return render(request, 'merma.html', {
                'message' : 'el registro fue Eliminado correctamente',
                'mermas': mermas,
            })
    

#crud Detalle Merma
@login_required
def registerDetalleMerma(request):
    if request.method == 'POST':
        producto = Producto.objects.get(id=request.POST.get('id_producto'))
        precio = producto.precio_unidad
        cantidad_venta = int(request.POST.get('cantidad'))
        cantidad_producto = producto.total_unidades
        total_pagar = precio * cantidad_venta
        # try: 
        id_merma = request.POST['id_merma']
        if int(request.POST.get('cantidad')) > cantidad_producto :

            return redirect('detalle_merma',id_merma)
        else:
            detMerma = Detalle_merma.objects.create(cantidad=request.POST['cantidad'], total=total_pagar, id_producto_id=request.POST['id_producto'], id_merma_id=request.POST['id_merma'])
            detMerma.save()
            merma = get_object_or_404(Merma, pk=request.POST['id_merma'])
            merma.total_merma = (merma.total_merma or 0) + total_pagar
            merma.save(update_fields=['total_merma'])
            cantidad = int(request.POST['cantidad']) 
            producto = get_object_or_404(Producto, pk=request.POST['id_producto'])
            producto.total_unidades = (producto.total_unidades or 0) - cantidad
            producto.save(update_fields=['total_unidades'])
            return redirect('detalle_merma',id_merma)
        # except:
        #     ventas = Venta.objects.all().order_by('id')
        #     estados = Estado_venta.objects.all()
        #     return render(request, 'ventas.html', {
        #         'error' : 'no se registro la venta',
        #         'estados': estados,
        #         'ventas' : ventas,
        #     })


@login_required
def deleteDetalleMerma(request,id_detalle_merma):
    
    detalleMerma = get_object_or_404(Detalle_merma,pk=id_detalle_merma)
    id_merma = detalleMerma.id_merma_id
    if request.method == 'POST':
        cantidad = int(detalleMerma.cantidad) 
        producto = get_object_or_404(Producto, pk=detalleMerma.id_producto_id)
        producto.total_unidades = (producto.total_unidades or 0) + cantidad
        producto.save(update_fields=['total_unidades'])
        detalleMerma.delete()
        return redirect('detalle_merma',id_merma)

def reportesProductos(request):
    user = request.user
    grupos_usuario = user.groups.all().values_list('name', flat=True)
    productos = Producto.objects.all().order_by('id_item_id')
    return render(request, 'reportes_producto.html',{
        'productos': productos,
        'grupos_usuario': grupos_usuario,
        'message': '',
        'error': ''
        })

def detallereportesProductos(request,id_producto):
    if request.method == 'GET':
        producto = get_object_or_404(Producto,pk=id_producto)
        items = Item.objects.all()
        det_lotes = Detalle_lote.objects.filter(id_producto_id=id_producto).order_by('id')
        lote = Lote.objects.all()
        det_ventas = Detalle_venta.objects.filter(id_producto_id=id_producto).order_by('id')
        venta = Venta.objects.all()
        total_ingreso = Detalle_lote.objects.filter(id_producto_id=id_producto).aggregate(Sum('cantidad'))['cantidad__sum']
        total_ventas = Detalle_venta.objects.filter(id_producto_id=id_producto).aggregate(Sum('cantidad'))['cantidad__sum']
        return render(request, 'detalleReporteProducto.html',{
            'product': producto,
            'items' : items,
            'det_lotes' : det_lotes,
            'lote': lote,
            'det_ventas' : det_ventas,
            'venta': venta,
            'total_ingreso' : total_ingreso,
            'total_ventas' : total_ventas
        })
    else : 
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Convertir las cadenas de fecha en objetos de fecha
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

        # Filtrar las ventas dentro del rango de fechas
        producto = get_object_or_404(Producto,pk=id_producto)
        items = Item.objects.all()
        lote = Lote.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
        venta = Venta.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
        det_lotes = Detalle_lote.objects.filter(id_producto_id=id_producto,id_lote_id__in =lote).order_by('id')
        
        det_ventas = Detalle_venta.objects.filter(id_producto_id=id_producto, id_venta_id__in = venta ).order_by('id')
        total_ingreso = Detalle_lote.objects.filter(id_producto_id=id_producto).aggregate(Sum('cantidad'))['cantidad__sum']
        total_ventas = Detalle_venta.objects.filter(id_producto_id=id_producto).aggregate(Sum('cantidad'))['cantidad__sum']

        return render(request, 'detalleReporteProducto.html',{
            'product': producto,
            'items' : items,
            'det_lotes' : det_lotes,
            'lote': lote,
            'det_ventas' : det_ventas,
            'venta': venta,
            'total_ingreso' : total_ingreso,
            'total_ventas' : total_ventas
        })


def reporteAlmacen(request):
    if request.method == 'GET':
        user = request.user
        grupos_usuario = user.groups.all().values_list('name', flat=True)
        lotes = Lote.objects.all().order_by('id')
        provedores = Proveedor.objects.all()
        users = User.objects.all()
        reingresos = Reingreso_lote.objects.all().order_by('id')
        total_ingreso = Lote.objects.count()
        total_reingreso = Reingreso_lote.objects.count()
        return render(request, 'reporte_almacen.html',{
        'reingresos': reingresos,
        'lotes' : lotes,
        'provedores' : provedores,
        'users' : users,
        'grupos_usuario': grupos_usuario,
        'total_ingreso' : total_ingreso,
        'total_reingreso' : total_reingreso,
        'message': '',
        'error': ''
        })
    else: 
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Convertir las cadenas de fecha en objetos de fecha
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()


        user = request.user
        grupos_usuario = user.groups.all().values_list('name', flat=True)
        lotes = Lote.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
        total_ingreso = Lote.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).count()
        provedores = Proveedor.objects.all()
        users = User.objects.all()
        reingresos = Reingreso_lote.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
        total_reingreso = Reingreso_lote.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).count()
        return render(request, 'reporte_almacen.html',{
        'reingresos': reingresos,
        'lotes' : lotes,
        'provedores' : provedores,
        'users' : users,
        'grupos_usuario': grupos_usuario,
        'total_ingreso' : total_ingreso,
        'total_reingreso' : total_reingreso,
        'message': '',
        'error': ''
        })


def reporteVentas(request):
    if request.method == 'GET':
        user = request.user
        grupos_usuario = user.groups.all().values_list('name', flat=True)
        ventas = Venta.objects.all().order_by('id')
        estados = Estado_venta.objects.all()
        users = User.objects.all()
        mermas = Merma.objects.all().order_by('id')
        total_ingreso = Lote.objects.count()
        total_ingreso_merma = Merma.objects.count()
        total_bs_venta = Venta.objects.all().aggregate(Sum('total_venta'))['total_venta__sum']
        producto_mas_vendido = Detalle_venta.objects.values('id_producto').annotate(total_vendido=Count('id_producto')).order_by('-total_vendido').first()
        producto_mas_vendido_obj = None
        if producto_mas_vendido:
            producto_mas_vendido_obj = Producto.objects.get(pk=producto_mas_vendido['id_producto'])
        return render(request, 'reporte_ventas.html',{
        'mermas': mermas,
        'ventas' : ventas,
        'estados' : estados,
        'users' : users,
        'grupos_usuario': grupos_usuario,
        'total_ingreso' : total_ingreso,
        'total_ingreso_merma' : total_ingreso_merma,
        'total_bs_venta': total_bs_venta,
        'producto_mas_vendido_obj' : producto_mas_vendido_obj,
        'message': '',
        'error': ''
        })
    else: 
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Convertir las cadenas de fecha en objetos de fecha
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()


        user = request.user
        grupos_usuario = user.groups.all().values_list('name', flat=True)
        estados = Estado_venta.objects.all()
        ventas = Venta.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
        total_ingreso = Venta.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).count()
        total_bs_venta = Venta.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).aggregate(Sum('total_venta'))['total_venta__sum']
        provedores = Proveedor.objects.all()
        users = User.objects.all()
        mermas = Merma.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
        total_ingreso_merma = Merma.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).count()
        producto_mas_vendido = Detalle_venta.objects.values('id_producto').annotate(total_vendido=Count('id_producto')).order_by('-total_vendido').first()
        producto_mas_vendido_obj = None
        if producto_mas_vendido:
            producto_mas_vendido_obj = Producto.objects.get(pk=producto_mas_vendido['id_producto'])
        return render(request, 'reporte_ventas.html',{
        'mermas': mermas,
        'estados': estados,
        'ventas' : ventas,
        'provedores' : provedores,
        'users' : users,
        'grupos_usuario': grupos_usuario,
        'total_ingreso' : total_ingreso,
        'total_ingreso_merma' : total_ingreso_merma,
        'total_bs_venta': total_bs_venta,
        'producto_mas_vendido_obj':producto_mas_vendido_obj,
        'message': '',
        'error': ''
        })




class PdfVenta(View):
    def link_callback(self, uri, rel):
        
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        # mUrl = settings.MEDIA_URL         # Typically /media/
        # mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        
        if uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
                return uri

         # make sure that file exists
        if not os.path.isfile(path):
                raise RuntimeError(
                        'media URI must start with %s or %s' % (sUrl)
                )
        return path

    def get(self, request, id_venta, *args,**kwargs):
        venta = get_object_or_404(Venta, pk=id_venta)
        productos = Producto.objects.all().order_by('id')
        estados = Estado_venta.objects.all()
        detventa = Detalle_venta.objects.filter(id_venta_id=id_venta).order_by('id')
        user = request.user
        # Renderizar la plantilla a HTML
        template = get_template('pdf_detalle_venta.html')
        context = {
            'venta': venta,
            'productos': productos,
            'estados': estados,
            'detventa': detventa,
            'user':user,
            'icon2' : '{}{}'.format(settings.STATIC_URL, 'img/4.jpg')

        }
        html = template.render(context)

        # Crear un archivo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="detalle_venta_{id_venta}.pdf"'

        # Convertir HTML a PDF
        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=self.link_callback)

        # Verificar si la conversión fue exitosa
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF')

        return response


class PdfAlmacen(View):
    def link_callback(self, uri, rel):
        
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        # mUrl = settings.MEDIA_URL         # Typically /media/
        # mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        
        if uri.startswith(sUrl):
                path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
                return uri

         # make sure that file exists
        if not os.path.isfile(path):
                raise RuntimeError(
                        'media URI must start with %s or %s' % (sUrl)
                )
        return path

    def get(self, request, id_lote, *args,**kwargs):
        lote = get_object_or_404(Lote,pk=id_lote)
        proveedores = Proveedor.objects.all()
        productos = Producto.objects.all().order_by('id')
        detLotes = Detalle_lote.objects.filter(id_lote_id =id_lote ).order_by('id')
        lotes = Lote.objects.all()
        user = request.user
        # Renderizar la plantilla a HTML
        template = get_template('pdf_detalle_almacen.html')
        context = {
            'lote': lote,
            'provedores': proveedores,
            'productos' : productos,
            'detLotes' : detLotes,
            'lotes' : lotes,
            'user': user,
            'icon' : '{}{}'.format(settings.STATIC_URL, 'img/3.jpg'),
            'icon2' : '{}{}'.format(settings.STATIC_URL, 'img/4.jpg')

        }
        html = template.render(context)

        # Crear un archivo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="detalle_lote_{id_lote}.pdf"'

        # Convertir HTML a PDF
        pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=self.link_callback)

        # Verificar si la conversión fue exitosa
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF')

        return response


