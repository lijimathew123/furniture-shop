from django.shortcuts import render,redirect,get_object_or_404
from .models import FurnitureCategory,FurnitureProduct,Promotion,BlogPost,ShoppingCart,CartItem,Review,Order
from django.contrib.auth import login, logout,authenticate
from django.contrib.auth.models import User

from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def register(request):
    user =None 
    error_message=None
    

    if request.POST:
        try:

            email = request.POST['email']
            username=request.POST['username']
            password = request.POST['password']

           

            user = User.objects.create_user(email=email,username=username,password=password)
            user.save()
            return redirect('user_login')
        except IntegrityError:
            error_message = "User with this email or username is already exist"
  
        
    return render(request,'register.html',{'user':user, 'error_message':error_message})



def user_login(request):
     user= None
     error_message =None
     if request.POST:
         username=request.POST['username']
         password = request.POST['password']
         user = authenticate(request,username=username,password=password)

         if user:
             login(request,user)
             return redirect('view_products')
         else:
             error_message ='Invalid credentials'
     return render(request,'login.html',{'error_message':error_message})
         

def user_logout(request):
    logout(request)
    return redirect('index')        
         
             


def index(request):
    product = FurnitureProduct.objects.all()[:4]
    promotion = Promotion.objects.all()
    trending = FurnitureProduct.objects.all()[2:5]
    return render(request,'index.html', {'products':product, 'promotions':promotion, 'trend':trending})


@login_required(login_url='user_login')
def view_products(request):
    
    products = FurnitureProduct.objects.all()
    return render(request, 'product.html',{'products':products})



def search_products(request):
    query = request.GET.get('q')

    if query:
        results = FurnitureProduct.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query)
        )
    else:
        results = FurnitureProduct.objects.all()

    return render(request,'product.html',{'products':results,'query':query})




def view_product_details(request,product_id):
    product = FurnitureProduct.objects.get(id=product_id)

    review =Review.objects.filter(product=product)
    return render(request,'product_details.html',{'products':product,'reviews':review})

def contact(request):
    return render(request,'contact.html')

def about_us(request):
    return render(request, 'about.html')

def view_blog(request):
    blog= BlogPost.objects.all()
    return render(request,'blog.html',{'blogs':blog})



@login_required(login_url='user_login')
def add_to_cart(request,product_id):
    product = get_object_or_404(FurnitureProduct, id=product_id)
    user=request.user
     
     #check if the user has a cart or create new one for that user
    shopping_cart, created = ShoppingCart.objects.get_or_create(user=user)
    
     
    #ckeck if the product is in that cart if no  then add product to that cart of that user
    cart_item,item_created = CartItem.objects.get_or_create(product=product, shopping_cart=shopping_cart)

     
     # if the product is already in the cart then add its quantity by 1
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

 
    return redirect('view_shopping_cart')



@login_required(login_url='user_login')
def view_shopping_cart(request):

    user=request.user

    shopping_cart,created = ShoppingCart.objects.get_or_create(user=user)
    
    #fetch cart details and Cart items
    cart_items = CartItem.objects.filter(shopping_cart=shopping_cart)

    for item in cart_items:
        item.total_amount = item.product.price * item.quantity

        
    total_quantity = sum(item.quantity  for item in cart_items)
    total_amount = sum(item.total_amount for item in cart_items)

    context = {
        'cart_items':cart_items,
        'total_quantity':total_quantity,
        'total_amount':total_amount,
    }
 
    return render(request,'shop-cart.html',context)



@login_required(login_url='user_login')
def remove_cart_item(request,item_id):
    item = get_object_or_404(CartItem,id=item_id)
    item.delete()

    return redirect('view_shopping_cart')

@login_required(login_url='user_login')
def add_review(request,product_id):
    user=request.user
    product=FurnitureProduct.objects.get(id=product_id)
    if request.POST:
        comment = request.POST['comment']


        review = Review.objects.create(user=user,comment=comment,product=product)
        review.save()


    return render(request,'index.html')



@login_required(login_url='user_login')
def buynow(request,item_id):
    user=request.user
    cart_item = get_object_or_404(CartItem, id=item_id, shopping_cart__user=user)
    total_amount = cart_item.product.price * cart_item.quantity

    context ={
        'total_amount':total_amount,
        'cart_item':cart_item,
        'razorpay_api_key':settings.RAZORPAY_API_KEY,
        'user':user
    }

    return render(request,'payment.html',context)


@csrf_exempt
def handle_payment(request):
    if request.method == 'POST':
        user = request.user
        product_name = request.POST.get('product_name')
        total_amount = request.POST.get('total_amount')
        payment_id = request.POST.get('payment_id')

       

        # Save the order
        order = Order.objects.create(
            user=user,
            product_name=product_name,
            total_amount=total_amount,
            payment_id=payment_id
        )

        return JsonResponse({'message': 'Payment successful', 'order_id': order.id})

    return JsonResponse({'message': 'Invalid request'}, status=400)