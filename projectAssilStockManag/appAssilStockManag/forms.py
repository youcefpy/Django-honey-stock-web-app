#forms

from django import forms
from .models import HoneyProduct, ProductBatch,Jar,JarBatch,FilledJar,Ticket,TicketBatch,Box,BoxBatch,FilledBox,Sku,SoldFilledJar,SoldFilledBox
from .constants import BOX_CONFIG
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class HoneyProductForm(forms.ModelForm):
    name_product = forms.CharField(label='Produit',max_length=255)
    class  Meta:
        model = HoneyProduct
        fields = ['name_product',]

class ProductBatchForm(forms.ModelForm):
    product = forms.ModelChoiceField(queryset=HoneyProduct.objects.all(), label='Produit')
    quantity_received = forms.DecimalField(label='Quantité reçue', max_digits=10, decimal_places=2)
    price_per_kg = forms.DecimalField(label='Prix par kg', max_digits=10, decimal_places=2)

    class Meta:
        model = ProductBatch
        fields = ['product','quantity_received','price_per_kg']


class ProductBatchUpdateForm(forms.ModelForm):
    class Meta:
        model = ProductBatch
        fields = ['quantity_received', 'price_per_kg']


class JarForm(forms.ModelForm):
    size = forms.ChoiceField(choices=Jar.JAR_SIZES, label='Taille Du Bocal')
    class Meta:
        model = Jar
        fields = ['size']

class JarBatchForm(forms.ModelForm):
    class Meta:
        model = JarBatch
        fields = '__all__'
        labels = {
            'jar':'Bocal',
            'date_received':'Date de reception',
            'quantity_received':'Quantiter recu',
            'price_jar':'prix par bocal',
        }

        
class FilledJarForm(forms.ModelForm):
    sku_code = forms.CharField(label='Sku', max_length=255, required=True)  # this is the search input
    sku_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # hidden field to store SKU ID
    class Meta:
        model = FilledJar
        fields = ['jar', 'product', 'quantity_field','sku_id']
        labels={
            'jar':'Bocal',
            'product':'Produit',
            'sku':'Sku',
            'quantity_field':'Quantiter Rempli',
        }

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
        labels={
            'type_ticket':'Type d\'etiquette',
            'product':'Produit',
        }

class TicketBatchForm(forms.ModelForm) :
    class Meta:
        model = TicketBatch
        fields = ['ticket','quantity_received','purchase_price']
        labels={
            'ticket':'Etiquette',
            'quantity_received':'Quantiter recu',
            'purchase_price':'Prix Etiquette',
        }


class BoxForm(forms.ModelForm):
    
    class Meta:
        model = Box
        fields = ['type_box']
        labels={
            'type_box':'Type de Coffret',
        }

class BoxBatchForm(forms.ModelForm):
    class Meta:
        model = BoxBatch
        fields  = ['box','quantity_received','purchase_price']
        labels={
            'box':'Coffret',
            'quantity_received':'Quantiter recu',
            'purchase_price':'prix d\'achat',
        }



class FilledBoxForm(forms.ModelForm):
    sku_code = forms.CharField(label='Sku', max_length=255, required=True)  # this is the search input
    sku_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)  # hidden field to store SKU ID
    class Meta:
        model = FilledBox
        fields = ['box_type','sku_id', 'quantity_fill_box']
        labels={
            'box_type':'Type de Coffret',
            'sku':'Sku',
            'quantity_fill_box':'Quantiter des coffret rempli',
        }
    def clean(self):
        cleaned_data = super().clean()
        for field in self.data:
            if '_' in field and '.' in field:
                # You can add more validation here if needed.
                cleaned_data[field] = self.data[field]
        return cleaned_data

    # def __init__(self, *args, **kwargs):
    #     super(FilledBoxForm, self).__init__(*args, **kwargs)
        
    #     for box_size, jars in BOX_CONFIG.items():
    #         for (jar_size, jar_type) in jars:
    #             field_name = f"{jar_type}_{jar_size}"
    #             self.fields[field_name] = forms.IntegerField(
    #                 required=True, 
    #                 label=f"Quantiter pour {jar_type.capitalize()} ({jar_size} KG)", 
    #                 initial=0,
    #                 min_value=0,
    #                 max_value=1,
    #                 widget=forms.NumberInput()
    #             )

class SkuForm(forms.ModelForm):
    class Meta:
        model = Sku
        fields = ['code','title'] 
        labels={
            'code':'Sku',
            'title':'Nom Produit',
        }


class SoldFilledJarForm(forms.ModelForm):
    class Meta:
        model = SoldFilledJar
        fields = '__all__' 

class SoldFilledBoxForm(forms.ModelForm):
    class Meta:
        model = SoldFilledBox
        fields = '__all__'
        labels={
            'filled_box':'TYPE COFFRET',
            'quantity_sell_box':'QUANTITER',
            'price_sell':'PRIX DE VENTE',

        }
        
