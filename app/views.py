from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from .models import * 
import json
from .models import Product, Order, OrderItem 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
#danh muc   
def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)

    context = {'categories': categories, 'products': products,'active_category':active_category}
    return render(request, 'app/category.html', context)

#search
def search(request):
    if request.method == 'POST':
     searched = request.POST["searched"]
     keys = Product.objects.filter(name__contains =  searched)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"

    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"

    products = Product.objects.all()
    
    return render(request,'app/search.html',{"searched":searched,"keys":keys,'products': products,'cartItems':cartItems,"user_not_login":user_not_login,"user_login":user_login})

# dang ky 
def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    user_not_login = "show"
    user_login = "hidden"
    context = {'form':form,"user_not_login":user_not_login,"user_login":user_login }
    return render(request,'app/register.html',context)

#dang nhap
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request,'user or password not correct!')
    user_not_login = "show"
    user_login = "hidden"
    context = {"user_not_login":user_not_login,"user_login":user_login}
    return render(request,'app/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

#trang chu
def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
        
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    products = Product.objects.all()
    context = {'products': products,'cartItems':cartItems,"user_not_login":user_not_login,"user_login":user_login,'categories':categories,}
    return render(request, 'app/home.html', context)

#gio hang 
def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer,complete =  False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    categories = Category.objects.filter(is_sub=False)
    context = {'categories':categories,'items':items,'order':order,'cartItems':cartItems,"user_not_login":user_not_login,"user_login":user_login}
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"

    context = {'items':items,'order':order,'cartItems':cartItems, "user_not_login":user_not_login,"user_login":user_login}
    return render(request, 'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    product = Product.objects.get(id=productId)
    
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity +1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)