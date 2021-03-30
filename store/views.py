from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json 
import datetime
from django import forms

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate , login,logout
from django.shortcuts import redirect
from .forms import ProductForm
from .forms import StoreForm
# Create your views here.

def store (request):

    if (request.user.is_authenticated):
        user = request.user
        customer, created  = Customer.objects.get_or_create( user=user , name = user.username)
        order ,created = Order.objects.get_or_create(customer=customer,complete=False)
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
    if productId != '':
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

    #this to delet the orderitem that has products removed
    if action =='removeOrder':
        item = data['item']
        itemr = OrderItem.objects.get(id=item)

        print(itemr)
        itemr.delete()
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


def page(request):
    if (request.user.is_authenticated):
        user = request.user
        customer  = Customer.objects.get(user=user)
        stores = Store.objects.filter(customer=customer)
        print(user)
       
        storeform = StoreForm(initial={'customer':customer},customer=user)
        #initcutomer = storeform.fields['customer'].queryset.filter(name=customer.name)
        #storeform.fields['customer'].queryset= initcutomer
        
        #these two lines of code were switched and made my life hell on earth holyshit
        productform = ProductForm(customer=customer)
        productform.fields['store'].queryset = stores
        products = []
        if request.method == 'POST':
            #print('printing POST : ',request.POST)
           
            if request.POST.get('addstore'):
                storeform = StoreForm(user,request.POST)
                if storeform.is_valid():
                    storeform.save()
                else :
                    print('not VALID FORGOT SOMTHING')

            elif request.POST.get('deletestore'):
                print('storedeleted')
                print(request.POST.get('storekey'))
                sk = request.POST.get('storekey')
                Store.objects.filter(pk=sk).delete()
            ### this to add products 

            elif request.POST.get('addproduct'):
                productform=ProductForm(customer,request.POST,request.FILES)
                if productform.is_valid():
                    productform.save()
                
            

            ### this to delete products 
            print(request.POST.get('key'))
            key = request.POST.get('key')
            Product.objects.filter(pk =key).delete()

        ## Resets the stores field
       # storeform.fields['customer'].queryset=initcutomer
        #storeform = StoreForm(initial={'customer':customer})
        #productform.fields['store'].queryset = stores
        if   stores.count == 0:
            print('cool')

            
        else:
            
            for s in stores :
                print(s.pk) 
                products += s.product_set.all()

        order , created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all() 
        cartItems = order.finalItemNum
      
    else:
        return redirect('login')
    context={'productform':productform,'stores':stores,'products':products,'isAuth':request.user.is_authenticated, 'cartitems':cartItems,'storeform':storeform}
    return render(request, 'store/page.html',context)

def addproduct(request):
    
    return JsonResponse('product added',safe=False)