from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json 
import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login,logout
from django.shortcuts import redirect
# Create your views here.

def store (request):

    if (request.user.is_authenticated):
        user = request.user
        customer  = Customer.objects.get(user=user)
        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all() 
        cartItems = order.finalItemNum
         
    else :
        items=[] 
        order = {'finalPrice':0 ,'finalItemNum':0}
        cartItems = order['finalItemNum']

    Products = Product.objects.all()
    context = {'products': Products , 'cartitems':cartItems,'isAuth':request.user.is_authenticated}
    return render(request,'store/store.html',context)

def cart (request):
    if (request.user.is_authenticated):
        user = request.user
        customer  = Customer.objects.get(user=user)

        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.finalItemNum  
    else :
        items=[] 
        order = {'finalPrice':0 ,'finalItemNum':0}
        cartItems = order['finalItemNum']
    
    context = {'items':items ,'order':order ,'cartitems':cartItems }
    return render(request,'store/cart.html',context)


def checkout (request):
    if (request.user.is_authenticated):
        user = request.user
        customer  = Customer.objects.get(user=user)

        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.finalItemNum  
    else :
        items=[] 
        order = {'finalPrice':0 ,'finalItemNum':0}
        cartItems = order['finalItemNum']
    context = {'items':items ,'order':order,'cartitems':cartItems}
    
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId= data['productId']
    action = data['action']
    print('the action is :',action)
    print('the productId is :',productId)

    user = request.user
    customer  = Customer.objects.get(user=user)

    product = Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderItem ,created = OrderItem.objects.get_or_create(order=order , product=product)


    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1 )
    elif action =='remove':
        orderItem.quantity = (orderItem.quantity - 1 )
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added',safe=False)

def processOrder(request):
    data = json.loads(request.body)
    
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        user = request.user
        customer  = Customer.objects.get(user=user)
        order=Order.objects.get(customer=customer,complete=False)
        items = order.orderitem_set.all() #the items in the order 
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        print(customer.name + ' made a purchase of :')
        for i in items:
            print(i.product.name + ' from ' + i.product.store.storename)
       
        if total ==order.finalPrice:
            order.complete = True
        order.save()
    else:
        print('user not authenticated')
    return JsonResponse('payment processed',safe=False)


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('login')
            
           
    
    context = {'form':form}
    return render(request,'store/register.html',context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username,password=password)
        print(username)
        if user is not None:
            login(request,user)
            customer,created = Customer.objects.get_or_create(user=user,name=username)
            customer.save()
            return redirect('store')
    context = {}
    return render(request,'store/login.html',context)
    
def logoutUser(request):
    logout(request)
    return redirect('store')


