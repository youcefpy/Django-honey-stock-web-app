from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Jar, HoneyProduct, FilledJar,ProductBatch,JarBatch,Ticket,TicketBatch,Box,BoxBatch,FilledBox,FilledBoxJars,SoldFilledJar,Sku
from django.db import transaction
from .forms import HoneyProductForm, ProductBatchForm,JarForm, JarBatchForm, FilledJarForm,TicketForm,TicketBatchForm,BoxForm,BoxBatchForm,FilledBoxForm,SkuForm,SoldFilledJarForm,ProductBatchUpdateForm,SignUpForm
from django.db.models import Sum
from .constants import BOX_CONFIG
from django.db import IntegrityError
from django.contrib import messages
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import login


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in.
            login(request, user)
            return redirect('login')  # or your desired redirect page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def add_honey_product(request):
    if request.method == "POST":
        form=HoneyProductForm(request.POST)
        if form.is_valid():   
            name_from_form = form.cleaned_data['name_product']
            if HoneyProduct.objects.filter(name_product=name_from_form).exists():
                messages.error(request,'Le produit exist deja dans la base de donne.')
            else : 
                form.save()
                # messages.success(request, 'Product added successfully!')
                return redirect('add_product_batch')          
    else:
        form = HoneyProductForm()
    context={
        'form':form,
    }
    return render(request,'add_honey_product.html',context)

@login_required
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

@login_required
def list_products(request):
    products = HoneyProduct.objects.all()
    return render(request, 'list_products.html', {'products': products})

@login_required
def delete_product(request,product_id):
    if not request.user.is_staff:  # Check if the user is staff (i.e., admin)
        return HttpResponseForbidden("You don't have permission to access this page.")
    if request.method == "POST":
        product = get_object_or_404(HoneyProduct,id = product_id)
        product.delete()
        return redirect('list_products')

@login_required
def update_product_batch(request,batch_id):
    batch = get_object_or_404(ProductBatch,id=batch_id)
    if request.method == "POST":
        form = ProductBatchUpdateForm(request.POST,instance = batch)

        if form.is_valid():
            form.save()
            return redirect('list_products')
    
    else : 
        form = ProductBatchUpdateForm(instance=batch)
    
    context = {
        'form': form,
        'batch_id': batch_id,
    }
    return render(request,'update_batch_product.html',context)


@login_required
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


@login_required
def add_jar(request):
    if request.method == 'POST':
        form = JarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jars_batch')
    else:
        form = JarForm()
    return render(request, 'add_jar.html', {'form': form})


@login_required
def add_jar_batch(request):
    if request.method == "POST":
        form = JarBatchForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('list_jars')
    else :
        form = JarBatchForm()
    return render(request,'add_jar_batch.html',{'form':form})

@login_required
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

@login_required
def add_filled_jar(request):
    if request.method == "POST":
        form = FilledJarForm(request.POST)

        if form.is_valid():
            jar = form.cleaned_data.get('jar')
            product = form.cleaned_data.get('product')
            quantity = form.cleaned_data.get('quantity_field')
            sku = form.cleaned_data.get('sku')

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
                    size=jar.size,
                    sku=sku
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

@login_required
def delete_filled_jar(request, filled_jar_id):
    if not request.user.is_staff:  # Check if the user is staff (i.e., admin)
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    if request.method == "POST":
        print(f"Attempting to delete filled jar with ID: {filled_jar_id}")
        filled_jar = get_object_or_404(FilledJar, id=filled_jar_id)
        try:
            with transaction.atomic():
                # Calculate honey to be added back
                honey_to_add = Decimal(filled_jar.jar.size) * Decimal(filled_jar.quantity_field)

                # Add back honey to HoneyProduct
                filled_jar.product.quantity_in_the_stock += honey_to_add
                filled_jar.product.save()
                print("Honey added back to HoneyProduct.")
            
                # Add back jars to Jar
                filled_jar.jar.quantity_in_the_stock += filled_jar.quantity_field
                filled_jar.jar.save()
                print("Jars added back.")

                # Add back the tickets
                ticket_type = f'{int(Decimal(filled_jar.jar.size) * 1000)}g'
                ticket_name = filled_jar.product.name_product
                try:
                    ticket = Ticket.objects.get(type_ticket=ticket_type, product__name_product=ticket_name)
                    ticket.quantity_in_the_stock += filled_jar.quantity_field
                    ticket.save()
                    print("Tickets added back.")
                except Ticket.DoesNotExist:
                    raise Exception(f"No ticket found for jar of size: {filled_jar.jar.size} and product: {filled_jar.product.name_product}")

                # Delete the FilledJar object
                filled_jar.delete()
                print("FilledJar object deleted.")

        except IntegrityError:
            messages.error(request, "Database integrity error.")
        except Exception as e:
            messages.error(request, f"Error deleting filled jar: {str(e)}")

        return redirect('list_filled_jars')

@login_required
def list_jars(request):
    jars = Jar.objects.all()
    return render(request, 'list_jars.html', {'jars': jars})

@login_required
def list_jars_filled(request):
    filled_jars = FilledJar.objects.all()
    aggregated_jars = FilledJar.objects.values('jar__size', 'product__name_product').annotate(total_jars=Sum('quantity_field')).order_by('jar__size', 'product__name_product')
    context = {
        'filled_jars':filled_jars,
        'aggregated_jars':aggregated_jars,
    }
    return render(request, 'list_filled_jars.html', context)


@login_required
def delete_jar(request, jar_id):
    if not request.user.is_staff:  # Check if the user is staff (i.e., admin)
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    if request.method == "POST":
        jar = get_object_or_404(Jar, id=jar_id)
        jar.delete()
        return redirect('list_jars')


@login_required
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

@login_required
def add_batch_ticket(request):
    if request.method == "POST":
        form = TicketBatchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_tickets')
    else : 
        form = TicketBatchForm()
    return render(request,'add_ticket_batch.html',{'form':form})

@login_required
def list_tickets(request):
    tickets = Ticket.objects.all()
    return render(request,'list_tickets.html',{'tickets':tickets})


@login_required
@transaction.atomic
def delete_ticket(request,ticket_id):
    if not request.user.is_staff:  # Check if the user is staff (i.e., admin)
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    ticket=get_object_or_404(Ticket,id=ticket_id)
    ticket.delete()
    return redirect('list_tickets')


@login_required
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

@login_required
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

@login_required
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

@login_required
def list_box(request):
    boxs = Box.objects.all()
    return render(request,'list_box.html',{'boxs':boxs})



@login_required
@transaction.atomic
def delete_box(request,box_id):
    if not request.user.is_staff:  # Check if the user is staff (i.e., admin)
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    box=get_object_or_404(Box,id=box_id)
    box.delete()
    return redirect('list_box')


@login_required
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

@login_required
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
                filled_box = FilledBox(box_type=box_type)    
                # print("Initial FilledBox quantity:", filled_box.quantity_fill_box)
                # Deduct the filled jars and boxes
                filled_box = filled_box.fill(filled_jars_data, box_quantity)

            except ValueError as e:
                messages.error(request,str(e))
                return redirect('add_fill_box')


            return redirect('list_filled_jars')
    else:
        form = FilledBoxForm()

    return render(request, 'add_fill_box.html', {'form': form})


@login_required
def list_filled_boxes(request):
    context = {}
    result = []

    all_boxes = FilledBox.objects.all().prefetch_related('filledboxjars_set__jar__product')

    box_aggregator = {}

    for box in all_boxes:
        # Create a set to ensure unique jars, so no repetition.
        unique_jars = set([f"{item.jar.product.name_product} ({item.jar.size}KG)" for item in box.filledboxjars_set.all()])
        jars_inside = " ".join(sorted(unique_jars))

        signature = f"{box.box_type.id}-{jars_inside}"

        if signature not in box_aggregator:
            box_aggregator[signature] = {
                'box_id': box.pk,
                'box_type': box.box_type,
                'jars_inside': jars_inside,
                'quantity': 0
            }

        box_aggregator[signature]['quantity'] += box.quantity_fill_box

    result = list(box_aggregator.values())

    context = {
        'result': result,
    }
    return render(request, 'list_filled_boxes.html', context)


@login_required
def delete_filled_box(request, fill_box_id):
    if not request.user.is_staff:  # Check if the user is staff (i.e., admin)
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    """
        When we delete the filled box, we will increment the quantity of filled jars 
        back to the FilledJar and also increment the box's quantity.
    """
    filled_box = get_object_or_404(FilledBox, id=fill_box_id)
    
    # Reconstruct the filled_jars_data based on the filled box
    filled_jars_data = [
        (item.jar.product.name_product, item.jar.size, item.quantity * filled_box.quantity_fill_box) 
        for item in filled_box.filledboxjars_set.all()
    ]

    # Re-add jars to the FilledJar stock
    for product_name, jar_size, total_jars_deleted in filled_jars_data:
        try:
            filled_jar = FilledJar.objects.get(jar__size=jar_size, product__name_product=product_name)
            filled_jar.quantity_field += total_jars_deleted
            filled_jar.save()
        except FilledJar.DoesNotExist:
            messages.error(request, f"No {product_name} jars of size {jar_size} KG in stock. Delete operation aborted.")
            return redirect('list_filled_boxes')

    # Increment the box's quantity in stock
    filled_box.box_type.quantity_in_stock += filled_box.quantity_fill_box
    filled_box.box_type.save()
    
    filled_box.delete()
    
    messages.success(request, "Filled Box deleted successfully!")
    return redirect('list_filled_boxes')


@login_required
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

@login_required
def add_sku(request):
    if request.method == "POST":
        form = SkuForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_sku')
        else : 
            print(form.errors)
    else :
        form = SkuForm()
    
    return render(request,'add_sku_product.html',{'form':form})

@login_required
def list_sku(request):
    list_sku = Sku.objects.all()
    context={
        "list_sku":list_sku,
    }
    return render(request,'list_sku.html',context)

@login_required
def add_sell_fill_jars(request):
    if request.method == "POST":
        form = SoldFilledJarForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_sell_jars')

    else:
        form = SoldFilledJarForm()
    context={
        'form':form
    }
    return render(request,'add_sell_filled_jars.html',context)

@login_required
def list_sell_jars(request):
    list_sell_jars =SoldFilledJar.objects.all()
    context={
        'list_sell_jars':list_sell_jars
    }
    return render(request,'list_sell_jars.html',context)
