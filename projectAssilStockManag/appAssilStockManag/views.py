from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Jar, HoneyProduct, FilledJar,ProductBatch,JarBatch,Ticket,TicketBatch,Box,BoxBatch,FilledBox
from django.db import transaction
from .forms import HoneyProductForm, ProductBatchForm,JarForm, JarBatchForm, FilledJarForm,TicketForm,TicketBatchForm,BoxForm,BoxBatchForm,FilledBoxForm
from django.db.models import Sum
from .constants import BOX_CONFIG
from django.db import IntegrityError
from django.contrib import messages
def add_honey_product(request):
    if request.method == "POST":
        form=HoneyProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_product_batch')

    else:
        form = HoneyProductForm()
    context={
        'form':form,
    }
    return render(request,'add_honey_product.html',context)

def add_product_batch(request):
    if request.method == "POST":
        form = ProductBatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_products')
    else : 
        form = ProductBatchForm()
    context = {
        'form':form,
    }
    return render(request,'add_product_batch.html',context)

def list_products(request):
    products = HoneyProduct.objects.all()
    return render(request, 'list_products.html', {'products': products})


def delete_product(request,product_id):
    if request.method == "POST":
        product = get_object_or_404(HoneyProduct,id = product_id)
        product.delete()
        return redirect('list_products')


@transaction.atomic
def delete_batch(request, batch_id):
    batch = get_object_or_404(ProductBatch, id=batch_id)
    product = batch.product

    
    total_cost_before = product.weighted_average_price * product.quantity_in_the_stock
    cost_of_this_batch = batch.price_per_kg * batch.quantity_received

    
    product.quantity_in_the_stock -= batch.quantity_received

    
    new_total_quantity = product.quantity_in_the_stock
    new_total_cost = total_cost_before - cost_of_this_batch
    
    if new_total_quantity > 0:
        new_weighted_avg = new_total_cost / new_total_quantity
    else:
        new_weighted_avg = 0
    
    batch.delete()
    return redirect('list_products')



def add_jar(request):
    if request.method == 'POST':
        form = JarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jars_batch')
    else:
        form = JarForm()
    return render(request, 'add_jar.html', {'form': form})



def add_jar_batch(request):
    if request.method == "POST":
        form = JarBatchForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('list_jars')
    else :
        form = JarBatchForm()
    return render(request,'add_jar_batch.html',{'form':form})

@transaction.atomic
def delete_jar_batch(request,batch_id):

    batch = get_object_or_404(JarBatch, id=batch_id)
    jar = batch.jar

    total_cost_before = jar.weighted_average_price * jar.quantity_in_the_stock
    cost_of_this_batch = batch.price_jar * batch.quantity_received

    
    jar.quantity_in_the_stock -= batch.quantity_received

    
    new_total_quantity = jar.quantity_in_the_stock
    new_total_cost = total_cost_before - cost_of_this_batch
    
    if new_total_quantity > 0:
        new_weighted_avg = new_total_cost / new_total_quantity
    else:
        new_weighted_avg = 0
    
    batch.delete()
    jar.save()
    return redirect('list_jars')
 
def add_filled_jar(request):
    if request.method == "POST":
        form = FilledJarForm(request.POST)

        if form.is_valid():
            jar = form.cleaned_data.get('jar')
            product = form.cleaned_data.get('product')
            quantity = form.cleaned_data.get('quantity_field')

            filled_jar = FilledJar.objects.filter(jar=jar, product=product).first()

            if filled_jar:
                filled_jar.quantity_field += quantity
                try:
                    filled_jar.save(update_stock=True)
                except ValueError as e:
                    messages.error(request, str(e))
                    return render(request, 'add_filled_jar.html', {'form': form})
                
                # Fetch the object from the database again and print
                updated_filled_jar = FilledJar.objects.get(id=filled_jar.id)
                print(f"Updated object from DB: {updated_filled_jar.quantity_field}")

            else:
                filled_jar = FilledJar(
                    jar=jar,
                    product=product,
                    quantity_field=quantity,
                    size=jar.size
                )
                try:
                    filled_jar.save(update_stock=True)
                except ValueError as e:   # Changed IntegrityError to ValueError
                    messages.error(request, str(e))
                    return render(request, 'add_filled_jar.html', {'form': form})

            return redirect('list_filled_jars')
        
        # For form errors
        for error in form.errors.values():
            messages.error(request, error)

    else:
        form = FilledJarForm()

    return render(request, 'add_filled_jar.html', {'form': form})



def list_jars(request):
    jars = Jar.objects.all()
    return render(request, 'list_jars.html', {'jars': jars})

def list_jars_filled(request):
    filled_jars = FilledJar.objects.all()
    aggregated_jars = FilledJar.objects.values('jar__size', 'product__name_product').annotate(total_jars=Sum('quantity_field')).order_by('jar__size', 'product__name_product')
    context = {
        'filled_jars':filled_jars,
        'aggregated_jars':aggregated_jars,
    }
    return render(request, 'list_filled_jars.html', context)



def delete_jar(request, jar_id):
    if request.method == "POST":
        jar = get_object_or_404(Jar, id=jar_id)
        jar.delete()
        return redirect('list_jars')



def add_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_batch_ticket')

    else :
        form = TicketForm()
    context = {
        'form':form
        }
    return render(request,'add_ticket.html',context)

def add_batch_ticket(request):
    if request.method == "POST":
        form = TicketBatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_tickets')
    else : 
        form = TicketBatchForm()
    return render(request,'add_ticket_batch.html',{'form':form})

def list_tickets(request):
    tickets = Ticket.objects.all()
    return render(request,'list_tickets.html',{'tickets':tickets})


@transaction.atomic
def delete_ticket(request,ticket_id):
    ticket=get_object_or_404(Ticket,id=ticket_id)
    ticket.delete()
    return redirect('list_tickets')

@transaction.atomic
def delete_ticket_batch(request, batch_id):
    batch = get_object_or_404(TicketBatch, id=batch_id)
    ticket = batch.ticket

    total_cost_before = ticket.weighted_average * ticket.quantity_in_the_stock
    cost_of_this_batch = batch.purchase_price * batch.quantity_received

    ticket.quantity_in_the_stock -= batch.quantity_received

    new_total_ticket = ticket.quantity_in_the_stock
    new_total_cost = total_cost_before - cost_of_this_batch

    if new_total_ticket > 0:
        new_weighted_avg = new_total_cost / new_total_ticket
    else:
        new_weighted_avg = 0

    batch.delete()

    return redirect('list_tickets')

def add_box(request):
    if request.method == "POST":
        form = BoxForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('add_box_batch')
    
    else :
        form = BoxForm()
    context = {
        'form':form
    }
    return render(request,'add_box.html',context)

def add_box_batch(request):
    if request.method =='POST':
        form = BoxBatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_box')
    else : 
        form =BoxBatchForm()
    context = {
        'form':form
    }
    return render(request,'add_box_batch.html',context)


def list_box(request):
    boxs = Box.objects.all()
    return render(request,'list_box.html',{'boxs':boxs})


@transaction.atomic
def delete_box(request,box_id):
    box=get_object_or_404(Box,id=box_id)
    box.delete()
    return redirect('list_box')

@transaction.atomic
def delete_box_batch(request, batch_id):
    batch = get_object_or_404(BoxBatch, id=batch_id)
    box = batch.box

    total_cost_before = box.weighted_average * box.quantity_in_stock
    cost_of_this_batch = batch.purchase_price * batch.quantity_received

    box.quantity_in_stock -= batch.quantity_received

    new_total_box = box.quantity_in_stock
    new_total_cost = total_cost_before - cost_of_this_batch

    if new_total_box > 0:
        new_weighted_avg = new_total_cost / new_total_box
    else:
        new_weighted_avg = 0

    batch.delete()

    return redirect('list_box')

def add_fill_box(request):
    if request.method == 'POST':
        form = FilledBoxForm(request.POST)
        if form.is_valid():           
            # Get the box type and its quantity
            box_type = form.cleaned_data['box_type']
            box_quantity = form.cleaned_data['quantity_fill_box']
            print(f'the quantity of the boxes is : {box_quantity}')
            
            # Construct the filled_jars_data list
            filled_jars_data = []
            for field_name, jars_quantity in form.cleaned_data.items():
                if '_' in field_name and '.' in field_name and jars_quantity > 0:
                    product_name, jar_size_str = field_name.rsplit('_', 1)
                    jar_size_str = float(jar_size_str.rstrip(" KG)"))
                    total_jars_needed = jars_quantity * box_quantity
                    filled_jars_data.append((product_name, jar_size_str, total_jars_needed))
            try : 

                # Create the filled box
                filled_box = form.save(commit=False)
                print("Initial FilledBox quantity:", filled_box.quantity_fill_box)
                # Deduct the filled jars and boxes
                filled_box.fill(filled_jars_data, box_quantity)

            except ValueError as e:
                messages.error(request,str(e))
                return redirect('add_fill_box')


            return redirect('list_filled_jars')
    else:
        form = FilledBoxForm()

    return render(request, 'add_fill_box.html', {'form': form})



def list_filled_boxes(request):
    filled_boxes = FilledBox.objects.all()
    return render(request, 'list_filled_boxes.html', {'filled_boxes': filled_boxes})


def main(request):
    products = HoneyProduct.objects.all()
    jars = Jar.objects.all()
    filledJars = FilledJar.objects.all()
    boxes = Box.objects.all()
    boxesFilled = FilledBox.objects.all()
    tickets = Ticket.objects.all()

    #extraction the name and th quantity of the product 
    product_name= [product.name_product for product in products]
    product_quantity = [product.quantity_in_the_stock for product in products]

    #extraction os the quantity and the size of the size 
    jar_size = [jar.size for jar in jars]
    jar_quantity = [jar.quantity_in_the_stock for jar in jars]

    #extraction os the quantity and the size of the size 
    ticket_type_prod = [f"{ticket.product.name_product} ({ticket.type_ticket})" for ticket in tickets]
    ticket_quantity = [ticket.quantity_in_the_stock for ticket in tickets]

    #extraction of the quantity and the name and the size of the filled_jars
    prod_with_jar =[f"{filledJar.product.name_product} ({filledJar.jar.size})" for filledJar in filledJars] 
    # fill_jar_size = [fillJar.jar.size for fillJar in filledJars]
    # prod_name = [filledJar.product.name_product for filledJar in filledJars]
    prod_quantity = [filledJar.quantity_field for filledJar in filledJars]
    
    #extraction of the quantity and the type of the box 
    box_type = [box.type_box for box in boxes]
    box_quantity = [box.quantity_in_stock for box in boxes]

    #extraction of the quantity and the type of filled box 
    fill_box_type = [str(boxFilled.box_type) for boxFilled in boxesFilled ]
    fill_box_quantity = [boxFilled.quantity_fill_box for boxFilled in boxesFilled]

    context = {
        'product_names': product_name,
        'product_quantities': product_quantity,
        'jar_size' : jar_size,
        'jar_quantity':jar_quantity,
        # 'fill_jar_size' : fill_jar_size,
        # 'prod_name':prod_name,
        'prod_with_jar':prod_with_jar,
        'prod_quantity':prod_quantity,
        'box_type':box_type,
        'box_quantity':box_quantity,
        'fill_box_type':fill_box_type,
        'fill_box_quantity':fill_box_quantity,
        'ticket_type':ticket_type_prod,
        'ticket_quantity':ticket_quantity,

    }
    return render(request,'main.html',context)

