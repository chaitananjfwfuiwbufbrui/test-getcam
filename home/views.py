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
from  django.contrib.auth.models import User 
from django.contrib.auth import logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from  django.contrib import messages


from datetime import datetime ,timedelta,date


# Create your views here.
def home(request): 
   
    if request.user.is_authenticated:
        now = datetime.now()
        last = date.today() - timedelta(days=30)
        timestamp = datetime.date(now)
        


        customer = request.user
        order ,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitems_set.all()
        cartitems = order.get_cart_item

        latest = products.objects.filter(pub_date__range=[last, timestamp])
            
        dataa = products.objects.all()
                
        context = {'dataa' : dataa,"latest":latest,'cartitems':cartitems}
    else:
        latest = products.objects.filter(pub_date__range=["2020-09-17", "2020-12-25"])
        
        dataa = products.objects.all()
        context = {'dataa' : dataa,"latest":latest}
    

    return render(request,'home.html',context)
    # return render(request,'home.html')
def cart(request):
    customer = request.user
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
    items = order.orderitems_set.all()
    cartitems = order.get_cart_item



    
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)
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
    transection_id = datetime.datetime.now().timestamp
    order ,created = Order.objects.get_or_create(customer=customer,complete=False)

    data = json.loads(request.body)
    total = float(data['form']['total'])
    order.transaction_id = transection_id
    print(transection_id)
    if total == order.get_cart_total:
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
    


    return render(request,'checkout.html',context)
def search(request):
    return render(request,'search.html')


def singleproduct(request,slug):
    if request.user.is_authenticated:
        
        customer = request.user
        order ,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitems_set.all()
        cartitems = order.get_cart_item
        
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
        
        context = {'single' : single,"prod":new_list,"catagory":newcat,'cartitems':cartitems}
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
            
        context = {'dataa' : dataa,'items':items,"latest":latest,'cartitems':cartitems}
        
        return render(request,'products.html',context)
    else:
         latest = products.objects.filter(pub_date__range=["2020-09-17", "2020-09-18"])
        
         dataa = products.objects.all()
            
         context = {'dataa' : dataa,"latest":latest}
        
         return render(request,'products.html',context)
       




#api
# def login(request):
#     if request.method == 'POST':
#        loginuser = request.POST['loginuser'] 
#        loginPassword= request.POST['loginPassword']
#        user = authenticate(username=loginuser,password=loginPassword)
#        if user is not None:
#             auth_login(request,user)
#             messages.success(request,"sucessfully login")
            
#             return redirect('home')
#        else:
#            messages.error(request,'invalid username')
#            return redirect('login')
  
#     return render(request,'login.html')
# def logouts(request):
#     logout(request)
#     messages.success(request,'successfully logout')
#     return redirect('home')
    



# def signin(request):
#     if request.method == 'POST':
#        user = request.POST['signupuser'] 
#        email = request.POST['signupemail']
#        signupfname = request.POST['signupfname']
#        signupsname = request.POST['signupsname']
#        pass1 = request.POST['inputPassword1']
#        pass2 = request.POST['inputPassword2']
#        if len(user) > 10:
#             messages.error(request,"user name should be less than 10 characters")
#             return redirect('home')
            
#        if pass1 != pass2:
#             messages.error(request,"passwoard should be match")
#             return redirect('home')

#        if not user.isalnum():
#             messages.error(request,"username must be in alphabhates and numaric")
#             return redirect('home')



#        myuser = User.objects.create_user(user,email,pass1)
#        myuser.first_name= signupfname
#        myuser.last_name = signupsname
#        myuser.save()
#        messages.success(request,"your account has been successfully created")
#        create_cus = Customer.objects.get_or_create(user=user,name=signupfname,email=email)
#        create_cus.save()
#        return redirect('signin')
       
#     else:
#         return render(request,'signinpage.html')  

       

