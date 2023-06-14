from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.forms import ModelForm
from .models import *

class ProductoForm(ModelForm):
    
    class Meta:
        model = Producto
        fields = ('nombre', 'stock', 'precio', 'descripcion', 'tipo','fechagregado','fechamodificado', 'foto')
        widgets = {'fechagregado' : forms.SelectDateWidget(years=range(2023,2027))}
        widgets = {'fechamodificado' : forms.SelectDateWidget(years=range(2023,2027))}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                Column('stock', css_class='form-group col-md-4 mb-0'),
                Column('precio', css_class='form-group col-md-4 mb-0'),
                Column('descripcion', css_class='form-group col-md-4 mb-0'),
                Column('tipo', css_class='form-group col-md-4 mb-0'),
                Column('fechagregado', css_class='form-group col-md-4 mb-0'),
                Column('fechamodificado', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar')
        )

class SusForm(ModelForm):
    
    class Meta:
        model = Suscripcion
        fields = ('nombrecompleto','apellidos','correo','numerotelefono','contraseña','confirmarcontraseña','numerotarjeta','fechavencimiento','cvv')
        
        widgets = {'fechavencimiento' : forms.SelectDateWidget(years=range(2023,2027))}
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('nombre completo', css_class='form-group col-md-4 mb-0'),
                Column('apellidos', css_class='form-group col-md-4 mb-0'),
                Column('correo', css_class='form-group col-md-4 mb-0'),
                Column('numero telefonico', css_class='form-group col-md-4 mb-0'),
                Column('contraseña', css_class='form-group col-md-4 mb-0'),
                Column('confirmar contraseña', css_class='form-group col-md-4 mb-0'),
                Column('numero de tarjeta', css_class='form-group col-md-4 mb-0'),
                Column('fechave ncimiento', css_class='form-group col-md-4 mb-0'),
                Column('cvv', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Guardar')
        )