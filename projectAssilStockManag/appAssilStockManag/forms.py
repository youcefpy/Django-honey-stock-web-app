#forms

from django import forms
from .models import HoneyProduct, ProductBatch,Jar,JarBatch,FilledJar,Ticket,TicketBatch,Box,BoxBatch,FilledBox
from .constants import BOX_CONFIG
class HoneyProductForm(forms.ModelForm):
    class  Meta:
        model = HoneyProduct
        fields = ['name_product',]

class ProductBatchForm(forms.ModelForm):
    class Meta:
        model = ProductBatch
        fields = ['product','quantity_received','price_per_kg']


class JarForm(forms.ModelForm):
    class Meta:
        model = Jar
        fields = '__all__'

class JarBatchForm(forms.ModelForm):
    class Meta:
        model = JarBatch
        fields = '__all__'

        
class FilledJarForm(forms.ModelForm):
    class Meta:
        model = FilledJar
        fields = ['jar', 'product', 'quantity_field']

    def clean(self):
        cleaned_data = super().clean()
        jar = cleaned_data.get('jar')
        product = cleaned_data.get('product')
        
        # Bypass the unique constraint validation
        if jar and product:
            try:
                filled_jar = FilledJar.objects.get(jar=jar, product=product)
                # If a filled jar already exists with this jar and product,
                # bypass the unique validation error
                self._errors.pop('jar', None)
                self._errors.pop('product', None)
            except FilledJar.DoesNotExist:
                pass
        return cleaned_data


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['type_ticket','product']

class TicketBatchForm(forms.ModelForm) :
    class Meta:
        model = TicketBatch
        fields = ['ticket','quantity_received','purchase_price']


class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = ['type_box']

class BoxBatchForm(forms.ModelForm):
    class Meta:
        model = BoxBatch
        fields  = ['box','quantity_received','purchase_price']


class FilledBoxForm(forms.ModelForm):
    class Meta:
        model = FilledBox
        fields = ['box_type']


class FilledBoxForm(forms.ModelForm):
    class Meta:
        model = FilledBox
        fields = ['box_type', 'quantity_fill_box'] 

    def __init__(self, *args, **kwargs):
        super(FilledBoxForm, self).__init__(*args, **kwargs)
        
        for box_size, jars in BOX_CONFIG.items():
            for (jar_size, jar_type) in jars:
                field_name = f"{jar_type}_{jar_size}"
                self.fields[field_name] = forms.IntegerField(
                    required=True, 
                    label=f"Quantity for {jar_type.capitalize()} ({jar_size} KG)", 
                    initial=0,
                    min_value=0,
                    max_value=1,
                    widget=forms.NumberInput()
                )
