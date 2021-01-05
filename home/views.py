from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from math import ceil
import json
import  datetime
# Create your views here.
from django.shortcuts import render,HttpResponse,redirect
from home.models import *
from items.models import *
from  django.contrib.auth.models import User 
from django.contrib.auth import logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from  django.contrib import messages


from datetime import datetime ,timedelta,date
import threading






# Create your views here.
def home(request): 
   
    if request.user.is_authenticated:
        #merchant acc
        group = None
        merchant = False
        print(request.user)
        user_name = request.user
        Profile.objects.get_or_create(user = user_name)
        if request.user.groups.exists():

            group = request.user.groups.all()[0].name
            if group == 'merchant':
                print(group)
                merchant = True
                
        


        now = datetime.now()
        last = date.today() - timedelta(days=30)
        timestamp = datetime.date(now)
        


        customer = request.user
        order ,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitems_set.all()
        cartitems = order.get_cart_item

        latest = products.objects.filter(pub_date__range=[last, timestamp])
            
        dataa = products.objects.all()
                
        context = {'dataa' : dataa,"latest":latest,'cartitems':cartitems,'chay':merchant}
    else:
        latest = products.objects.filter(pub_date__range=["2020-09-17", "2021-12-25"])
        
        dataa = products.objects.all()
        context = {'dataa' : dataa,"latest":latest}
    

    return render(request,'home.html',context)
    # return render(request,'home.html')
def cart(request):
    customer = request.user
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitems_set.all()
    cartitems = order.get_cart_item



    
    items = order.orderitems_set.all()
    context = {'items':items,'order':order,'cartitems':cartitems}


    return render(request,'cart.html',context)


def updatecart(request):
    data = json.loads(request.body)
    productid = data['productsid']
    action = data['action']
    
    customer = request.user
    product = products.objects.get(id=productid)
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderitems ,created = Orderitems.objects.get_or_create(order=order,product=product)
    cartitems = order.get_cart_item
    if action == 'add':
        
        orderitems.quantity = (orderitems.quantity + 1)

    elif action == "remove":
            orderitems.quantity = (orderitems.quantity-1)
    elif action == 'delete':
        orderitems.quantity = 0


    orderitems.save()
    if orderitems.quantity <= 0 :
            orderitems.delete()
    

    return JsonResponse("your cart is added",safe=False)



def processorder(request):
    print('data:',request.body)
    customer = request.user
    transection_id = datetime.now().timestamp
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)

    data = json.loads(request.body)
    total = float(data['form']['total'])
    order.transaction_id = transection_id
    print(transection_id)
    if total == order.get_cart_total:
        order.complete = True
    order.complete = True
    order.save()

    if order.complete == True:
        ShippingOrder.objects.create(
            customer = customer,
            order = order,
            
            address =data['shipping']['address'],
            city = data['shipping']['country'],

            zipcode = data['shipping']['zip'],
            
            state =  data['shipping']['state'],
        )
         
    return JsonResponse("payment has been done....",safe=False)




def check(request):
    return render(request,'check.html')

def checkout(request):
    customer = request.user
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitems_set.all()
    cartitems = order.get_cart_item
    context = {'items':items,'order':order,'cartitems':cartitems}
    
    if profile_and_phnumberchecker(request,customer,"welcome to check out enter the details to process order") is False:
        
    
        return render_page(request,customer,"to get in to checkout page")
    print(profile_and_phnumberchecker(request,customer,"welcome to check out enter the details to process order") )
    return render(request,'checkout.html',context)
def search(request):
    return render(request,'search.html')



def singleproduct(request,slug):
    if request.user.is_authenticated:
        
        customer = request.user
        order ,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitems_set.all()
        cartitems = order.get_cart_item


        #algo for pricing 
        s = products.objects.filter(slug=slug).first()
        print(s.product_name)
        single = s 
        imageya = images_fiels.objects.filter(product = single)
        print(single.id)
        


        all_obj = products.objects.filter(product_name=s.product_name)


        #algo for pricing ^^^^^^
        slugsad = str(slug)




        #cart check 
        orde = Order.objects.filter(customer = customer).first()
        prod = Orderitems.objects.filter(order = orde)
        already_ther = False
        for i in prod:
            if i.product.slug == slug:

                already_ther = True
            





        prod = products.objects.filter(sub_category=single.sub_category)
        subheading = products.objects.filter(category=single.category)
        
        removelis = [single.product_name]
        new_list = []
        newcat = []
        #filtering single product from our sub catagiory set
        for i in prod:
            if not i.product_name in removelis:
                new_list.append(i)
        #filtering single product from our sub catagiory set            
        for s in subheading:
            if not s.product_name in removelis:
                newcat.append(s)
        #filtering sub catagiory  product from our catagiory set
        for q in new_list:
            if q in newcat:
                newcat.remove(q)
        
        context = {'single' : single,"prod":new_list,"catagory":newcat,'cartitems':cartitems,"imageya":imageya,"all_obj":all_obj,"already_ther":already_ther,"slugsad":slugsad}
        return render(request,'singleproduct.html',context)

    else:
    
        single = products.objects.filter(slug=slug).first()
        
        
        prod = products.objects.filter(sub_category=single.sub_category)
        subheading = products.objects.filter(category=single.category)
        
        removelis = [single.product_name]
        new_list = []
        newcat = []
        #filtering single product from our sub catagiory set
        for i in prod:
            if not i.product_name in removelis:
                new_list.append(i)
        #filtering single product from our sub catagiory set            
        for s in subheading:
            if not s.product_name in removelis:
                newcat.append(s)
        #filtering sub catagiory  product from our catagiory set
        for q in new_list:
            if q in newcat:
                newcat.remove(q)
        
        context = {'single' : single,"prod":new_list,"catagory":newcat}
        return render(request,'singleproduct.html',context)


def provider(request):
    if request.method =="POST":
            selected_provider = request.POST['cars']
            print(selected_provider)
            return redirect(f"/single/{selected_provider}")

 
    
def tracker(request):
    product = products.objects.all()
    print(product)
    n = len(product)
    nSlides = n//4 + ceil((n/4)-(n//4))
    params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': product}
    return render(request, 'tracker.html', params)

    
        

    return render(request,'tracker.html',context)
def user(request):

    
    product= products.objects.all()
    allProds=[]
    catprods= products.objects.values('sub_category', 'id')
    cats= {item["sub_category"] for item in catprods}
    for cat in cats:
        prod=products.objects.filter(sub_category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params={'allProds':allProds }
    return render(request,"tracker.html", params)

    

    
def Contact(request):
    if request.method =="POST":
            name = request.POST['Name']
            email = request.POST['Email']
            phn = request.POST['Phoneno']
            desc = request.POST['Message']
               
              
            ins = contact(name=name,desc=desc,phn=phn,email=email)
            ins.save()
            messages.success(request,"your details has been recorded")



    
    return render(request,'contact.html')

def productss(request):
       
    if request.user.is_authenticated:
        
        customer = request.user
        order ,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitems_set.all()
        cartitems = order.get_cart_item


        latest = products.objects.filter(pub_date__range=["2020-09-17", "2020-09-18"])
        
        dataa = products.objects.all()



        user_of = Profile.objects.get(user=request.user)
        phone_verified = user_of.phone_verified 
        profile_verified = user_of.profile_verified  



        
        context = {'dataa' : dataa,'items':items,"latest":latest,'cartitems':cartitems,'phone_verified':phone_verified,"profile_verified":profile_verified}
        
        return render(request,'products.html',context)
    else:
         latest = products.objects.filter(pub_date__range=["2020-09-17", "2020-09-18"])
        
         dataa = products.objects.all()
            
         context = {'dataa' : dataa,"latest":latest}
        
         return render(request,'products.html',context)
       


def merchant(request):
        from django.contrib.auth.models import Group
        user = request.user
        group = Group.objects.get(name='merchant')
        user_of = Profile.objects.get(user=request.user)
        print(user_of.phone_verified)
        # if profile_and_phnumberchecker(request,user,"merchant account created","to create merchant account"):
        #     user.is_staff=True

        #     user.groups.add(group)
        #     user.save()
        # else:
        #     profile_and_phnumberchecker(request,user,"merchant account created","to create merchant account")

          

        if user_of.phone_verified and user_of.profile_verified :



            user.is_staff=True

            user.groups.add(group)
            user.save()
            messages.success(request,"merchant account created !!")
        else:
            if user_of.phone_verified is  False:

                messages.info(request,"verify your phone number  create merchant account")
                return redirect('phone')
            if user_of.profile_verified is  False:

                messages.info(request,"verify your  profile to create merchant account")
                return redirect('adhar')

    
        return redirect('home')


def profile_and_phnumberchecker(request,us,succes):
        user_of = Profile.objects.get(user=us)
        x = False 
        if user_of.phone_verified and user_of.profile_verified :


            messages.success(request,f"{succes}!!")
            x = True
            return x
        else:
            return x
def render_page(request,us,fails):
            user_of = Profile.objects.get(user=us)
            if user_of.phone_verified is  False:

                messages.info(request,f"verify your phone number  {fails}")
                return redirect("/auth/phone")
            if user_of.profile_verified is  False:

                messages.info(request,f"verify your  profile {fails}")
                return redirect('adhar')