from django.shortcuts import render,redirect,get_object_or_404
# from django.http import HttpResponse
from .models import Book,Cart
from .forms import BookForm,Registration,CustomLoginForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
stripe.api_key=settings.STRIPE_SECRET_KEY
from django.urls import reverse


# Create your views here.
def home(request):
    # return HttpResponse("<h1>Welcome to App1 Home<h2>")
    # a=['Apple','Orange','Kiwi','Grapes']
    return render(request,'APP1/Home.html')



def about(request):
    # return HttpResponse("<h1>welcome to APP1 about<h2>")
    return render(request,'APP1/About.html')


def contact(request):
    return render(request,'APP1/Contact.html')

@login_required
def view(request):
    a=Book.objects.all()
    return render(request,'APP1/View.html',{"table":a})

@login_required
def createbook(request):
    a=BookForm(request.POST or None,request.FILES or None)
    if a.is_valid():
        a.save()
        return redirect(view)
    return render(request,'APP1/createbook.html',{"forms":a})

@login_required
def update(request,id):
    a=Book.objects.get(id=id)
    form=BookForm(request.POST or None, request.FILES or None,instance=a)
    if form.is_valid():
        form.save()
        return redirect(view)
    return render(request,'APP1/update.html',{"forms":form})

@login_required
def delete(request,id):
    a=Book.objects.get(id=id)
    if request.method=="POST":
        a.delete()
        return redirect(view)
    return render(request,'APP1/delete.html',{"forms":a})


def Register(request):
    a=Registration(request.POST or None)
    if request.method=="POST" and a.is_valid():
        a.save()
        return redirect(view)
    return render(request,'APP1/register.html',{"forms":a})

def LoginForm(request):
    a=CustomLoginForm(request,data=request.POST or None)
    if request.method=="POST" and a.is_valid():
        b=a.get_user()
        login(request,b)
        return redirect(view)
    return render(request,'APP1/loginform.html',{"forms":a})
    
def logout_view(request):
    logout(request)
    return redirect("login")

def cart(request):
    a=Cart.objects.filter(user=request.user)
    return render(request,'APP1/cart.html',{'cart':a})

def add_cart(request,book_id):
    a=Book.objects.get(id=book_id)
    item,created=Cart.objects.get_or_create(book=a,user=request.user)
    if not created:
        item.quantity+=1
        item.save()
    return redirect("cart")

# def cart_dlt(request,book_id):
#     a=Book.objects.get(id=book_id)
#     item,created=Cart.objects.get_or_create(book=a,user=request.user)
#     if not created:
#         if item.quantity>1:
#             item.quantity-=1
#             item.save()
#         else:
#             item.delete()
#     return redirect("cart")

def buy_now(request,book_id):
    cart_items=get_object_or_404(Cart,user=request.user,id=book_id)
    book=cart_items.book

    session=stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data':{
                    'currency':'inr',
                    'product_data':{
                        'name':book.name,
                    },
                    'unit_amount':int(float(book.price)*100),

                },
                'quantity':cart_items.quantity,
            }
            
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("success")),
        cancel_url=request.build_absolute_uri(reverse("cart"))

    )  
    return redirect(session.url)  


def success(request):
    return render(request,'APP1/success.html')

