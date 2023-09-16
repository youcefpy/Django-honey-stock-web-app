from django.db import models
from decimal import Decimal
from django.db import transaction
from django.db.models import Count
import logging



class HoneyProduct(models.Model):
    name_product=models.CharField(max_length=255,unique=True)
    quantity_in_the_stock= models.DecimalField(max_digits=10,decimal_places=2,default=0)
    date_entry = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name_product

    @property
    def total_quantity(self):
        return sum([batch.quantity_received for batch in self.productbatch_set.all()])

    @property
    def weighted_average_price(self):
        total_cost = sum([batch.price_per_kg * batch.quantity_received for batch in self.productbatch_set.all()])
        total_qty = sum([batch.quantity_received for batch in self.productbatch_set.all()])

        if total_qty == 0: 
            return 0

        return total_cost / total_qty
    

class ProductBatch(models.Model):
    product = models.ForeignKey(HoneyProduct,on_delete=models.CASCADE)
    date_received = models.DateField(auto_now_add=True)
    quantity_received = models.DecimalField(max_digits=10,decimal_places=2)
    price_per_kg = models.DecimalField(max_digits=10,decimal_places=2)

    def save(self, *args, **kwargs):
        product = HoneyProduct.objects.get(id=self.product.id)
        if not self.pk:  # If this is a new batch
            product.quantity_in_the_stock += self.quantity_received
        else:  # If this is an update
            old_batch = ProductBatch.objects.get(id=self.id)
            product.quantity_in_the_stock -= old_batch.quantity_received  # remove old quantity
            product.quantity_in_the_stock += self.quantity_received  # add new quantity
        product.save()
        super(ProductBatch, self).save(*args, **kwargs)

    @property
    def total_price(self):
        return self.quantity_received * self.price_per_kg
    def __str__(self):
        return f"{self.quantity_received} - {self.price_per_kg}"

class Jar(models.Model):
    JAR_SIZES = [
        (0.01,'10g'),
        (0.1,'100g'),
        (0.125, '125g'),
        (0.2, '200g'),
        (0.25, '250g'),
        (0.5, '500g'),
    ]
    size = models.FloatField(choices=JAR_SIZES,unique=True)
    quantity_in_the_stock = models.IntegerField(default=0)
    
    @property
    def total_jars_received(self):
        return sum([batch.quantity_received for batch in self.jarbatch_set.all()])
    
    @property
    def weighted_average_price(self):
        total_cost = sum([batch.price_jar * batch.quantity_received for batch in self.jarbatch_set.all()])
        total_qty = sum([batch.quantity_received for batch in self.jarbatch_set.all()])

        if total_qty == 0:
            return 0

        return total_cost / total_qty
    
    def __str__(self) -> str:
        return f'{self.size}'

class JarBatch(models.Model):
    jar = models.ForeignKey(Jar,on_delete=models.CASCADE)
    date_received = models.DateField(auto_now_add=True)
    quantity_received = models.DecimalField(max_digits=10,decimal_places=2)
    price_jar = models.DecimalField(max_digits=10,decimal_places=2)

    def save(self, *args, **kwargs):
        if not self.pk:  
            jar = Jar.objects.get(id=self.jar.id)
            jar.quantity_in_the_stock += self.quantity_received
            jar.save()
        super(JarBatch, self).save(*args, **kwargs)

    @property
    def total_price(self):
        return self.quantity_received * self.price_jar
   

class Sku(models.Model):
    code  =  models.CharField(max_length=255,unique=True)
    title =  models.CharField(max_length=255)

    def __str__(self) :
        return f"{self.code}"

class FilledJar(models.Model):
    jar = models.ForeignKey(Jar, on_delete=models.CASCADE)
    product = models.ForeignKey(HoneyProduct, on_delete=models.CASCADE)
    quantity_field= models.PositiveBigIntegerField()
    filled_date = models.DateField(auto_now_add=True)
    size = models.DecimalField(max_digits=5, decimal_places=3)
    sku = models.ForeignKey(Sku,on_delete=models.CASCADE,null=True, blank=True)

    def save(self, update_stock=False, *args, **kwargs):
        if  update_stock:
            if not self.jar.size or not self.quantity_field:
                raise ValueError("Either jar size or quantity field is None. Please check your data.")

            product_amount_required = Decimal(float(self.jar.size) * self.quantity_field)

            # Check if there is enough of honey in the stock
            if self.product.quantity_in_the_stock < product_amount_required:
                raise ValueError("Pas assez de produit en stock pour remplir les pots")

            # Check if there is enough quantity of Jars in the stock 
            if self.jar.quantity_in_the_stock < self.quantity_field:
                raise ValueError('Pas assez de bocale pour le remplisage')

            
            # Manage ticket stock
            ticket_type = f'{int(self.jar.size * 1000)}g' 
            ticket_name = self.product.name_product
            try:
                ticket = Ticket.objects.get(type_ticket=ticket_type,product__name_product=ticket_name)
                if ticket.quantity_in_the_stock < 0 :
                    raise ValueError ('Pas assez d\'etiquette dans le stock')
            except Ticket.DoesNotExist:
                raise ValueError(f"No ticket found for type: {ticket_type}")

            if ticket.quantity_in_the_stock <= 0:
                raise ValueError("Not enough tickets in stock.")

            # Deduct from stocks
            ticket.quantity_in_the_stock -= self.quantity_field
            self.product.quantity_in_the_stock -= product_amount_required
            self.jar.quantity_in_the_stock -= self.quantity_field

            ticket.save()
            self.product.save()
            self.jar.save()

        super(FilledJar, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} ({self.size}KG)"

class Ticket(models.Model):
    TYPE_CHOICES = [
        ('10g','10g'),
        ('100g','100g'),
        ('125g','125g'),
        ('200g','200g'),
        ('250g','250g'),
        ('500g','500g'),
    ]
    type_ticket = models.CharField(max_length=50,choices=TYPE_CHOICES)
    quantity_in_the_stock = models.IntegerField(default=0)
    date_entry = models.DateField(auto_now_add=True)
    product = models.ForeignKey(HoneyProduct, on_delete=models.CASCADE)
    @property
    def weighted_average(self):
        total_coast = sum([batch.quantity_received * batch.purchase_price for batch in self.ticketbatch_set.all()])
        total_quantity= sum([batch.quantity_received for batch in self.ticketbatch_set.all()])

        if total_quantity == 0 :
            return 0 
        return total_coast / total_quantity

    def __str__(self):
        return f"{self.product.name_product} {self.type_ticket}"

class TicketBatch(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE)
    quantity_received = models.DecimalField(max_digits=10,decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10,decimal_places=2)
    date_entry = models.DateField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.pk: 
            ticket = Ticket.objects.get(id=self.ticket.id)
            ticket.quantity_in_the_stock += self.quantity_received
            ticket.save()
        super(TicketBatch, self).save(*args, **kwargs)
    
    @property
    def total_price(self):
        return self.quantity_received * self.purchase_price

    def __str__(self):
        return f"{self.ticket}"


class Box(models.Model):
    COFFRET_TYPES = [
        ('coffret 3500', 'coffret 3500'),
        ('coffret 4000', 'coffret 4000'),
        ('coffret 4500', 'coffret 4500'),
        ('coffret 7500', 'coffret 7500'),
        ('coffret 8500', 'coffret 8500'),
        ('coffret 9900', 'coffret 9900'),
    ]
    type_box = models.CharField(max_length=50, choices=COFFRET_TYPES, unique=True)
    quantity_in_stock = models.IntegerField(default=0)

    @property
    def weighted_average(self):
        total_coast = sum([batch.quantity_received * batch.purchase_price for batch in self.boxbatch_set.all()])
        total_quantity= sum([batch.quantity_received for batch in self.boxbatch_set.all()])

        if total_quantity == 0 :
            return 0 
        return total_coast / total_quantity

    def __str__(self):
        return self.type_box



class BoxBatch(models.Model):
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    quantity_received = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=100,decimal_places=2)
    date_entry = models.DateField(auto_now_add=True)

    def save(self,*args,**kwargs):
        if not self.pk:
            box = Box.objects.get(id=self.box.id)
            box.quantity_in_stock += self.quantity_received
            box.save()
        super(BoxBatch,self).save(*args,**kwargs)
    
    @property
    def total_price(self):
        return self.quantity_received * self.purchase_price

    def __str__(self):
        return f"{self.box}"


class FilledBox(models.Model):
    box_type = models.ForeignKey(Box, on_delete=models.CASCADE)
    filled_jars = models.ManyToManyField(FilledJar, through='FilledBoxJars')
    fill_date = models.DateField(auto_now_add=True)
    quantity_fill_box = models.PositiveIntegerField(default=0)
    jars_signature = models.CharField(max_length=255, blank=True, null=True)
    sku = models.ForeignKey(Sku,on_delete=models.CASCADE,null=True,blank=True)

    @transaction.atomic
    def fill(self, filled_jars_data, box_quantity):
        # Calculate the jars signature
        jars_signature = "-".join(sorted([f"{product_name}-{jar_size}" for product_name, jar_size, _ in filled_jars_data]))
        similar_filled_box = FilledBox.objects.filter(box_type=self.box_type, jars_signature=jars_signature).first()
        
        if similar_filled_box:
            # Increment the quantity if similar box exists
            similar_filled_box.quantity_fill_box += box_quantity
            similar_filled_box.save()
            box_for_operations = similar_filled_box
        else:
            # Create new record if not exists
            self.jars_signature = jars_signature
            self.quantity_fill_box = box_quantity
            self.save()
            box_for_operations = self

        # Deduct jars from the FilledJar model and associate with FilledBox
        for product_name, jar_size, total_jars_needed in filled_jars_data:
            try:
                filled_jar = FilledJar.objects.get(jar__size=jar_size, product__name_product=product_name)
                # filled_jar.quantity_field = int(filled_jar.quantity_field)
                total_jars_needed = int(total_jars_needed)
                # Ensure we have enough stock in FilledJars

                print(f"Available {product_name} jars of size {jar_size}KG: {filled_jar.quantity_field}")
                print(f"Total jars needed: {total_jars_needed}")

                if filled_jar.quantity_field < total_jars_needed:
                    raise ValueError(f"Not enough {product_name} jars of size {jar_size} KG in stock to fill the boxes.")
                
                # Decrease from filled jar stock
                filled_jar.quantity_field -= total_jars_needed
                filled_jar.save()

                # Associate jar with box
                filled_box_jar, _ = FilledBoxJars.objects.get_or_create(box=box_for_operations, jar=filled_jar)
                filled_box_jar.quantity = total_jars_needed
                filled_box_jar.save()
                
            except FilledJar.DoesNotExist:
                raise ValueError(f"No {product_name} jars of size {jar_size} KG in stock.")
        
        # Decrease box from the stock
        self.box_type.quantity_in_stock -= box_quantity
        self.box_type.save()

    def __str__(self):
        return f"{self.box_type}"

# A model to keep track of the jars in each filled box, and their respective quantities
class FilledBoxJars(models.Model):
    box = models.ForeignKey(FilledBox, on_delete=models.CASCADE)
    jar = models.ForeignKey(FilledJar, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class SoldFilledJar(models.Model):
    filled_jar = models.ForeignKey(FilledJar, on_delete=models.CASCADE)
    sold_date = models.DateField(auto_now_add=True)
    quantity_sell_jars = models.IntegerField(default=1)
    price_sell = models.DecimalField(max_digits=10,decimal_places=2)
    
    def total_price(self):
        return self.quantity_sell_jars * self.price_sell
    
    def save(self,*args,**kwargs):
        super(SoldFilledJar,self).save(*args,**kwargs)

        self.filled_jar.quantity_field -= self.quantity_sell_jars 
        self.filled_jar.save()


class SoldFilledBox(models.Model):
    filled_box  = models.ForeignKey(FilledBox, on_delete=models.CASCADE)
    sold_date = models.DateField(auto_now_add=True)
    quantity_sell_box = models.IntegerField(default=1)
    price_sell = models.DecimalField(max_digits=10,decimal_places=2)
    
    def total_price(self):
        return self.quantity_sell_box * self.price_sell
    
    def save(self,*args,**kwargs):
        if self.filled_box.quantity_fill_box >= self.quantity_sell_box:
            super(SoldFilledBox, self).save(*args, **kwargs)  # Call the "real" save() method.

            #decrease the quantity of filled_jars : 
            self.filled_box.quantity_fill_box -= self.quantity_sell_box
            self.filled_box.save()
        else : 
            raise ValueError("Pas Assez de coffret rempli dans le stock")