from django.shortcuts import render,redirect
from DM_APP.models import Slider,Banner_Area,Main_Category,Product,Category,Color,Brand,CouponCode
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max, Min, Sum
from cart.cart import Cart





def base(request):
    return render(request, 'base.html')

def home(request):
    sliders = Slider.objects.all().order_by('-id')[0:3]
    banners = Banner_Area.objects.all().order_by('-id')[0:3]
    main_category = Main_Category.objects.all()
    product = Product.objects.filter(section__name = "Top Deals Of The Day")
    context = {
        'sliders' : sliders,
        'banners' : banners,
        'main_category' : main_category,
        'product':product,
        
    }
    return render(request, "main/home.html",context)



def product_details(request,slug):
    product = Product.objects.filter(slug = slug)
    if product.exists():
        product = Product.objects.get(slug = slug)
    else:
        return redirect('404')
    context = {
        'product' : product,
    }
    return render(request, "product/product_detail.html",context)


def error404(request):
    return render(request,'error/404.html')

def my_account(request):
    return render(request, 'account/my_account.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if user.objects.filter(username = username).exists():
            messages.error(request,"Username already exists! Please try another one.")
            return redirect("login") 
        
        if user.objects.filter(username = username).exists():
             messages.error(request,"Email already exists! Please try another one.")
             return redirect("login")
         
        user = User(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()       
        return redirect('login')


def Login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Email and Password Are Invalid !!')
            return redirect('login')
    # return render(request, 'account/my_account.html')

@login_required(login_url = '/accounts/login/')
def profile(request):
    return render(request, 'profile/profile.html')

def UpdateProfile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id
        
        user  = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        
        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile are Successfully Updated')
        return redirect('profile')
        

@require_POST
def logout_view(request):
    logout(request)
    return redirect('home') 


def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def product(request):
    category = Category.objects.all()
    product = Product.objects.all()
    brand = Brand.objects.all()
    min_price = Product.objects.all().aggregate(Min('price'))
    max_price = Product.objects.all().aggregate(Max('price'))
    FilterPrice = request.GET.get('FilterPrice')
    color = Color.objects.all()
    ColorID = request.GET.get('colorID')
    if FilterPrice:
        Int_FilterPrice = int(FilterPrice)
        product = Product.objects.filter(price__lte = Int_FilterPrice)
    elif ColorID:
        product = Product.objects.filter(color =  ColorID)
    else:
        product = Product.objects.all()
        
    context = {
        'category' : category,
        'product' : product,
        'min_price' : min_price,
        'max_price' : max_price,
        'FilterPrice':FilterPrice,
        'color' : color,
        'brand' : brand,
    }
    return render(request, 'product/product.html', context)


def filter_data(request):
    categories = request.GET.getlist('category[]')
    # brands = request.GET.getlist('brand[]')
    brand = request.GET.getlist('brand[]')
    product_num = request.GET.getlist('product_num[]')

    allProducts = Product.objects.all().order_by('-id').distinct()
    if len(categories) > 0:
        allProducts = allProducts.filter(Categories__id__in=categories).distinct()

    # if len(brands) > 0:
    #     allProducts = allProducts.filter(Brand__id__in=brands).distinct()
        
    if len(brand) > 0:
        allProducts = allProducts.filter(Brand__id__in=brand).distinct()
        
    if len(product_num) > 0:
        allProducts = allProducts.all().order_by('-id')[0:1]


    t = render_to_string('ajax/product.html', {'product': allProducts})

    return JsonResponse({'data': t})






@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
# def cart_detail(request):
#     # Ensure 'cart' session variable exists and is not None
#     cart = request.session.get('cart', {})
    
#     # Calculate packing cost and tax only if 'cart' is not empty
#     if cart:
#         packing_cost = sum(i.get('packing_cost', 0) for i in cart.values())
#         tax = sum(i.get('tax', 0) for i in cart.values())
#     else:
#         packing_cost = 0
#         tax = 0
    
#     valid_coupon = None
#     coupon = None
#     if request.method == 'GET':
#         coupon_code = request.GET.get('coupon_code')
#         if  coupon_code:
#             try:
#                 coupon = CouponCode.objects.get(code = coupon_code)
#                 valid_coupon = 'Are Applicable on Current Order !'
#             except:
#                 invalid_coupon = 'Invalid Coupon Code'
#     context = {
#         'packing_cost': packing_cost,
#         'tax': tax,
#         'coupon' : coupon,
#         'valid_coupon' : valid_coupon,
#         'invalid_coupon' : invalid_coupon,
        
#     }
#     return render(request, 'cart/cart.html', context)


def cart_detail(request):
    # Ensure 'cart' session variable exists and is not None
    cart = request.session.get('cart', {})
    
    # Calculate packing cost and tax only if 'cart' is not empty
    if cart:
        packing_cost = sum(i.get('packing_cost', 0) for i in cart.values())
        tax = sum(i.get('tax', 0) for i in cart.values())
    else:
        packing_cost = 0
        tax = 0
    
    valid_coupon = None
    coupon = None
    invalid_coupon = None  # Define invalid_coupon with a default value
    if request.method == 'GET':
        coupon_code = request.GET.get('coupon_code')
        if coupon_code:
            try:
                coupon = CouponCode.objects.get(code=coupon_code)
                valid_coupon = 'Coupon is applicable on the current order!'
            except CouponCode.DoesNotExist:
                invalid_coupon = 'Invalid Coupon Code'
    
    context = {
        'packing_cost': packing_cost,
        'tax': tax,
        'coupon': coupon,
        'valid_coupon': valid_coupon,
        'invalid_coupon': invalid_coupon,
    }
    return render(request, 'cart/cart.html', context)


def checkout(request):
    coupon_discount = None
    if request.method == "POST":
        coupon_discount = request.POST.get('coupon_discount')
    cart = request.session.get('cart',{})
    if cart:
        packing_cost = sum(i.get('packing_cost', 0) for i in cart.values())
        tax = sum(i.get('tax', 0) for i in cart.values())
    else:
        packing_cost = 0
        tax = 0
    
    tax_and_packing_cost = (packing_cost + tax)
    context = {
        'tax_and_packing_cost' : tax_and_packing_cost,
        'coupon_discount' : coupon_discount,
    }
    return render(request, 'checkout/checkout.html',context)