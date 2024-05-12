from django import forms
from .models import Producto
from .models import Proveedor
from .models import Lote
from .models import Detalle_lote
from .models import Venta
from .models import Reingreso_lote
from .models import Detalle_reingreso
from .models import Merma
from .models import Detalle_merma
from django.contrib.auth.models import User,Group

class UserForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['password','is_superuser','username','first_name','last_name','email']
        widgets = {
            'groups': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'u_medida', 'peso', 'precio_unidad', 'id_item','total_unidades']

class ProvedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'celular', 'direccion', 'profesion']

class LoteForm(forms.ModelForm):
    class Meta:
        model = Lote
        fields = ['n_lote', 'fecha','fecha_vencimiento', 'id_user', 'id_proveedor']

class DetLoteForm(forms.ModelForm):
    class Meta:
        model = Detalle_lote
        fields = ['cantidad', 'id_lote', 'id_producto']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['id_user','nombre_cliente','nit', 'fecha','tipo_venta',  'id_estado','total_venta']

class ReingresoLoteForm(forms.ModelForm):
    class Meta: 
        model = Reingreso_lote
        fields = [ 'fecha','detalle', 'id_user']

class DetReinForm(forms.ModelForm):
    class Meta:
        model = Detalle_reingreso
        fields = ['cantidad', 'id_reingreso_lote', 'id_producto']

class MermaForm(forms.ModelForm):
    class Meta:
        model = Merma
        fields = ['id_user','descripcion', 'fecha','total_merma']

class DetMermaForm(forms.ModelForm):
    class Meta:
        model = Detalle_merma
        fields = ['cantidad', 'id_merma', 'id_producto','total']