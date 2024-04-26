
from  django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render,redirect
from math import ceil
from pyexpat.errors import messages
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, ProductForm, FeedbackForm
from .models import Registration, Admin, Product, Cart, CartItem


def indexfunction(request):
    return render(request,"index.html")

def sparepart(request):
    current_user = request.user
    print(current_user)
    allProds = []
    catprods = Product.objects.values('category','id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod= Product.objects.filter(category=cat)
        n=len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params= {'allProds':allProds}
    return render(request,'Spareparts.html',params)





@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    user_id = request.user.id

    # Retrieve or create the cart associated with the authenticated user
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Create or retrieve the cart item
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')




def view_cart(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart/view_cart.html', {'cart_items': cart_items, 'cart': cart})

@login_required
def checkout(request):
    # Assuming the user is authenticated
    if request.user.is_authenticated:
        try:
            # Retrieve the user's cart and associated cart items
            cart = Cart.objects.get(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            # Perform your checkout logic here
            # For example: create an order, process payment, etc.

            # Create a list to store information about purchased items
            purchased_items = []

            for cart_item in cart_items:
                purchased_items.append({
                    'product': cart_item.product,
                    'quantity': cart_item.quantity,
                    'total_price': cart_item.get_total(),
                })

            # Clear the cart items and the entire cart
            cart_items.delete()
            cart.delete()

            # Pass the purchased items information to the template
            return render(request, 'view_cart.html', {'purchased_items': purchased_items})

        except Cart.DoesNotExist:
            # Handle the case where the user doesn't have a cart
            return HttpResponse("No items in the cart")

    else:
        # Handle the case where the user is not authenticated
        return HttpResponse("Authentication required to proceed with checkout")

def registration(request):
    form = RegistrationForm()

    if request.method == "POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "Successfully Registered"
            return render(request,"regsuccess.html",{"msg":msg})
        else:
            return HttpResponse("Registration Failed")

    return render(request,"registration.html",{"form":form})
def userlogin(request):
    return render(request,"userlogin.html")
def viewprodectsinad(request):
    return render(request,"viewprodectsinad.html")

def checkuserlogin(request):
    emailid=request.POST["emailid"]
    pwd=request.POST["password"]

    flag=Registration.objects.filter( Q(email=emailid) & Q(password=pwd) )

    if flag:
        return render(request,"userhome.html")
    else:
        msg="Login Failed"
        return render(request, "userlogin.html",{"msg":msg})

def userhome(request):
    return render(request,"userhome.html")

def userlogout(request):
    return render(request,"userlogin.html")
def newproject(request):
    return render(request,"newproducts.html")
def addproduct(request):
    auname = request.session["auname"]
    form = ProductForm()
    if request.method == "POST":
        formdata = ProductForm(request.POST,request.FILES)
        if formdata.is_valid():
            formdata.save()
            msg="Product Added Successfully"
            return render(request, "addproduct.html", {"auname":auname,"productform": form,"msg":msg})
        else:
            msg = "Failed to Add Product"
            return render(request, "addproduct.html", {"auname":auname,"productform": form, "msg": msg})
    return render(request,"addproduct.html",{"auname":auname,"productform":form})
def adminhome(request):
    auname=request.session["auname"]
    return render(request,"adminhome.html")

def viewaproducts(request):
    auname=request.session["auname"]
    productlist = Product.objects.all()
    count = Product.objects.count()
    return render(request,"viewaproducts.html",{"auname":auname,"productlist":productlist,"count":count})

def adminlogin(request):
    return render(request,"adminlogin.html")

def checkadminlogin(request):
    uname = request.POST["ausername"]
    pwd = request.POST["apassword"]

    flag = Admin.objects.filter(Q(username__exact=uname) & Q(password__exact=pwd))
    print(flag)

    if flag:
        admin = Admin.objects.get(username=uname)
        print(admin)
        request.session["auname"] = admin.username
        return render(request, "adminhome.html", {"auname": admin.username})
    else:
        msg = "Login Failed"
        return render(request, "adminlogin.html", {"msg": msg})

def adminlogout(request):
    return render(request,"adminlogin.html")

def displayeproducts(request):

    eid=request.session["eid"]
    ename=request.session["ename"]

    pname = request.POST["pname"]
    print(pname)

    productlist = Product.objects.filter(name__icontains=pname)

    return render(request,"displayeproducts.html",{"eid": eid, "ename": ename,"productlist":productlist})


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'feedback_thanks.html')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})
