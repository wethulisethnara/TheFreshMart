from urllib import request
from django.http import JsonResponse
from django.shortcuts import render ,redirect
from .models import *
from .forms import*  # type: ignore
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from .forms import LoginForm, ContactForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect, get_object_or_404
from .models import Item, Order
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm

# Create your views here.

@login_required
def unitview(request):
    units = unit.objects.all()
    paginator = Paginator(units, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.method =='POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UnitForm()
    context = {'form':form,'page':page}
    return render(request, 'unit.html', context)

@login_required
def categoryview(request):
    categories = category.objects.all()  # Fetching all category objects
    paginator = Paginator(categories, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    
    if request.method =='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CategoryForm()
    context = {'form':form,'cats':categories,'page':page}
    return render(request, 'category.html', context)


def itemsview(request):
    items = Item.objects.all()
    paginator = Paginator(items, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.method =='POST':
        form = ItemForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    else:
        form = ItemForm()
    context = {'form':form,'items':items, 'page':page}
    return render(request, 'items.html', context)


def itemview(request,pk):
    item = Item.objects.get(id=pk)
    return render(request,'item.html',{'item':item})

@login_required
def supplierview(request):
    suppliers = Supplier.objects.all()
    paginator = Paginator(suppliers, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.method == "POST":
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            form = SupplierForm()
            return redirect(f'/app/supplier/?page={page_number}')
    else:
        form = SupplierForm()
    context = {'form':form,'page':page}
    return render(request,'supplier.html',context)

@login_required
def orderview(request):
    # Filter orders for customers and suppliers
    customer_orders = Order.objects.filter(customer__isnull=False)
    supplier_orders = Order.objects.filter(supplier__isnull=False)

    # Pagination for customer orders
    customer_paginator = Paginator(customer_orders, 3)
    customer_page_number = request.GET.get('customer_page')
    customer_page = customer_paginator.get_page(customer_page_number)

    # Pagination for supplier orders
    supplier_paginator = Paginator(supplier_orders, 3)
    supplier_page_number = request.GET.get('supplier_page')
    supplier_page = supplier_paginator.get_page(supplier_page_number)

    # Handle form submission
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            form = OrderForm()
            return redirect('order')  # Redirect to the same page after saving
    else:
        form = OrderForm()

    context = {
        'form': form,
        'customer_page': customer_page,
        'supplier_page': supplier_page,
    }
    return render(request, 'order.html', context)

def homeview(request):
    return render (request,'index.html')

def shopview(request):
    categories = category.objects.all() 
    items = Item.objects.all()
    paginator = Paginator(categories, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = {'items':items, 'page':page}
    return render (request,'shop.html', context)


def loginview(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.groups.filter(name='Cashier').exists():
                    return redirect('home')  # Redirect to cashier page
                else:
                    return redirect('home')  # Redirect to user page
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logoutview(request):
    # Log out the user
    if request.method == 'POST':
        logout(request)
        return redirect('home')  # You can replace 'home' with the URL name of your home page
    else:
        return render(request, 'logout.html')

@login_required
def update_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        try:
            form = ItemForm(request.POST, request.FILES,instance=item)
            if form.is_valid():
                form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Item updated successfully!',
                    'updatedItem': {
                        'name': item.name,
                        'price': item.price,
                        'image_url': item.image.url,
                        'description': item.description,
                        'catergory':item.category.name,
                        'unit':item.unit.name,
                    },
                })
            else:
                return JsonResponse({'success': False, 'message': 'Invalid form data.'})
        except Item.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Item not found.'})
    else:
        form = ItemForm(instance=item)
    return render(request, 'update_form.html', {'form': form})

@login_required
def delete_confirm(request, item_id):
    item = Item.objects.get(id=item_id)
    return render(request, 'delete_confirm.html', {'item': item})

@login_required
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    if request.method == 'POST':
        item.delete()
        return JsonResponse({'success': True, 'message': 'Item deleted successfully!'})
    return redirect('itemview')

@login_required
def update_catergory(request, catergory_id):
    catergory = category.objects.get(id=catergory_id)
    current_page = request.GET.get('page', 1)  # Default to page 1 if not provided
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=catergory)
        if form.is_valid():
            form.save()
            # Redirect to the category view with the current page
            return redirect(f'/app/category/?page={current_page}')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form data.'})
    else:
        form = CategoryForm(instance=catergory)
    return render(request, 'update_catergory_form.html', {'form': form, 'current_page': current_page})

@login_required
def delete_confirm_category(request, category_id):
    current_page = request.GET.get('page', 1)
    cat = category.objects.get(id=category_id)
    return render(request, 'delete_confirm_category.html',  {'cat': cat, 'current_page': current_page})

@login_required
def delete_catergory(request, category_id):
    catergory= category.objects.get(id=category_id)
    current_page = request.GET.get('page', 1)
    if request.method == 'POST':
        catergory.delete()
    return redirect(f'/app/category/?page={current_page}')

@login_required
def update_unit(request, unit_id):
    uts = unit.objects.get(id=unit_id)
    current_page = request.GET.get('page', 1)  # Default to page 1 if not provided
    if request.method == 'POST':
        form = UnitForm(request.POST, instance=uts)
        if form.is_valid():
            form.save()
            # Redirect to the unit view with the current page
            return redirect(f'/app/unit/?page={current_page}')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form data.'})
    else:
        form = UnitForm(instance=uts)
    return render(request, 'update_unit_form.html', {'form': form, 'current_page': current_page})

@login_required
def delete_confirm_unit(request, unit_id):
    current_page = request.GET.get('page', 1)
    uts = unit.objects.get(id=unit_id)
    return render(request, 'delete_confirm_unit.html',  {'uts': uts, 'current_page': current_page})

@login_required
def delete_unit(request, unit_id):
    uts= unit.objects.get(id=unit_id)
    current_page = request.GET.get('page', 1)
    if request.method == 'POST':
        uts.delete()
    return redirect(f'/app/unit/?page={current_page}')

@login_required
def update_order(request, order_id):
    oder = Order.objects.get(id=order_id)
    current_page = request.GET.get('page', 1)  # Default to page 1 if not provided
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=oder)
        if form.is_valid():
            form.save()
            # Redirect to the order view with the current page
            return redirect(f'/app/order/?page={current_page}')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form data.'})
    else:
        form = OrderForm(instance=oder)
    return render(request, 'update_order_form.html', {'form': form, 'current_page': current_page})

@login_required
def delete_confirm_order(request, order_id):
    current_page = request.GET.get('page', 1)
    oder = Order.objects.get(id=order_id)
    return render(request, 'delete_confirm_order.html',  {'oder': oder, 'current_page': current_page})

@login_required
def delete_order(request, order_id):
    oder= Order.objects.get(id=order_id)
    current_page = request.GET.get('page', 1)
    if request.method == 'POST':
        oder.delete()
    return redirect(f'/app/order/?page={current_page}')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Prepare the email content
            admin_email = settings.EMAIL_HOST_USER
            email_subject = f"New Contact Form Submission: {subject}"
            email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

            # Send the email
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=email,
                recipient_list=[admin_email],
            )

            # Show success message
            return render(request, 'contact.html', {
                'form': ContactForm(),  # Empty form after success
                'success': 'Thank you for your message! We will get back to you soon.',
            })
    else:
        form = ContactForm()

    return render(request, 'contact.html',{'form':form})

def product_buy(request, pk):
    item = get_object_or_404(Item, id=pk)  # Ensure the item exists
    if request.method == 'POST':
        form = buy(request.POST)
        if form.is_valid():
            # Extract customer name and mobile number from the form
            customer_name = form.cleaned_data['customer_name']
            mobile = form.cleaned_data['mobile']

            # Dynamically create or get a customer
            customer, created = Customer.objects.get_or_create(
                mobileno=mobile,
                defaults={'name': customer_name},  # Use provided customer name
            )

            # Save the order
            order = form.save(commit=False)
            order.customer = customer  # Assign the customer to the order
            order.save()  # Save the order first to get a primary key
            
            # Use the set() method to assign the item to the many-to-many field
            order.item.set([item])  # Use a list or queryset to set items
            
            return redirect('shop')  # Redirect to the shop or success page
    else:
        form = buy()
    context = {'form': form, 'item': item}
    return render(request, 'product_buy.html', context)


def get_or_create_cart(request): 
    session_key = request.session.session_key 
    if not session_key: 
        request.session.create() 
        session_key = request.session.session_key 
    cart, created = Cart.objects.get_or_create(session_key=session_key) 
    return cart

def add_to_cart(request, product_id): 
    product = get_object_or_404(Item, id=product_id) 
    cart = get_or_create_cart(request) 
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product) 
    if not created: 
        cart_item.quantity = F('quantity') + 1  # Use F to avoid race conditions 
    cart_item.save() 
    return redirect('cart_detail') 

def cart_detail(request): 
    cart = get_or_create_cart(request) 
    items = cart.items.all() 
    total_price = cart.get_total_price() 
    return render(request, 'cart_detail.html', {'cart': cart, 'items': items, 'total_price': total_price})

def update_cart_item(request, item_id): 
    if request.method == 'POST': 
        cart_item = get_object_or_404(CartItem, id=item_id, cart__session_key=request.session.session_key) 
        quantity = int(request.POST.get('quantity', 1)) 
        if quantity > 0: 
            cart_item.quantity = quantity 
            cart_item.save() 
    return redirect('cart_detail')

def remove_from_cart(request, item_id): 
    cart_item = get_object_or_404(CartItem, id=item_id, cart__session_key=request.session.session_key) 
    cart_item.delete() 
    return redirect('cart_detail')

@login_required
def update_supplier(request, supplier_id):
    supplier = Supplier.objects.get(id=supplier_id)
    current_page = request.GET.get('page', 1)  # Default to page 1 if not provided
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            # Redirect to the category view with the current page
            return redirect(f'/app/supplier/?page={current_page}')
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form data.'})
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'update_supplier_form.html', {'form': form, 'current_page': current_page})

@login_required
def delete_confirm_supplier(request, supplier_id):
    current_page = request.GET.get('page', 1)
    supplier = Supplier.objects.get(id=supplier_id)
    return render(request, 'delete_confirm_supplier.html',  {'supplier': supplier, 'current_page': current_page})

@login_required
def delete_supplier(request, supplier_id):
    supplier= Supplier.objects.get(id=supplier_id)
    current_page = request.GET.get('page', 1)
    if request.method == 'POST':
        supplier.delete()
    return redirect(f'/app/supplier/?page={current_page}')
