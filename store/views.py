from django.shortcuts import render, redirect
from .models import Product , OrderItem , ShippingAddress , FullOrder , Purchased_item, sendEmail, FaceShape
from .models import ProductCategories, Prescription
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ShippingForm , ShippingUpdateForm, FaceShapeForm, PrescriptionAddForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , HttpResponseRedirect ,Http404
from django.urls import reverse
from . import ObserverPattern
import datetime
import json
from .FaceShapes import face_shapes
from .SimpleFactory import sunglassesDisp, lensDisp, framesDisp
from ecommerce.settings import STATIC_DIR

SUN_CONST = 3
LENS_CONST = 6
FRAMES_CONST = 11
# Create your views here.
def store(request):

    total_item_cart = 0

    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity
    product_categories = ProductCategories.objects.all()
    context = {
        'product_categories' : product_categories,
        'total_item_cart' : total_item_cart,
    }
    return render(request, 'store/store.html', {'context':context})

def opto(request):

    if (request.user.groups.all() and  request.user.groups.first().name =='Optometrist'):
        full_orders = FullOrder.objects.all()
        pres_orders = Prescription.objects.all()
        return render(request, 'store/opto.html', {'full_orders' : full_orders, 'pres_orders' : pres_orders})
    else:
        return HttpResponseRedirect(reverse('store'))



def checkout(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))
    items = []
    total_cost_cart = 0
    total_item_cart = 0

    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

        for item in items:
            total_cost_cart += item.get_total

    if total_item_cart == 0:
        return Http404

    count_bfr = ShippingAddress.objects.filter(user = request.user).count()
    form = ShippingForm()
    if request.method == 'POST':
        form = ShippingForm(request.POST)
        if form.is_valid():
            adr = form.save(commit=False)
            adr.user = request.user
            adr.save()
        count_aftr = ShippingAddress.objects.filter(user = request.user).count()
        
        return HttpResponseRedirect(reverse('checkout'))

    addresses = ShippingAddress.objects.filter(user = request.user)
    
    product_categories = ProductCategories.objects.all()

    context = {
        'product_categories' : product_categories,
        'total_item_cart': total_item_cart,
        
    }
    return render(request, 'store/checkout.html', {'context':context, 'items': items,'total_cost_cart': total_cost_cart, 'form' : form,'addresses' : addresses})



@csrf_exempt
def insert_into_cart(request):
    if request.method == 'POST': 
        form = PrescriptionAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    total_item_cart = 0
    about = 'item_not_added'
    if request.user.is_authenticated:
        #print('skm')
        about = 'Item Added'
        #import pdb;pdb.set_trace()
        product_id = request.POST.get('product_id')
        product_category_id = request.POST.get('product_category_id')
        print("prod Id",product_id)
        #print("ID",product_category_id)
        print("Req",request)
        product = Product.objects.get(id = product_id)
        product_category  = ProductCategories.objects.filter(product=product)
        #product_category_id = ProductCategories.objects.get(id=request.id)
        #for product_category in product_category:
            #print(product_category)
        ##########################################################################
        #if OrderItem.objects.filter(product=product,user = request.user).exists():
         #   item = OrderItem.objects.get(product=product,user = request.user)
          #  if product_category == "Frames":
           # item.quantity = item.quantity+2
            #item.save()

        if OrderItem.objects.filter(product=product,user = request.user).exists():
            item = OrderItem.objects.get(product=product,user = request.user)
            #print(product_category)
            if product_category == "<QuerySet [<ProductCategories: Frames>]>":
                print(product_category)
                item.quantity = item.quantity+2
                item.save()
            else:
                print('skm') 
                item.quantity += 1
                item.save()
        else:
            item = OrderItem.objects.create(product=product,user = request.user,quantity =1)
            item.save()

        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity
        #import pdb;pdb.set_trace()
        if(product_category_id == FRAMES_CONST):
            framesDisp().post_prescription_details(request)
        print("CAt in insert",product_category_id)

    dic = {
        'data' : about,
        'total_item_cart' : total_item_cart,
    }
    return JsonResponse(dic, safe=False)

@csrf_exempt
def update_item_quantity(request):
    about = 'Some Error Occurred'
    if request.user.is_authenticated:
        about = 'Item Updated'
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        product = Product.objects.get(id=product_id)
        item = OrderItem.objects.get(product=product, user=request.user)

        if action == 'add':
            item.quantity+=1
        else:
            item.quantity-=1
        item.save()
        if item.quantity <= 0 :
            item.delete()

    dic = {
        'data': about,
    }
    return JsonResponse(dic,safe=False)



def cart(request):

    items = []
    total_cost_cart=0
    total_item_cart=0

    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user = request.user)
        for item in items:
            total_item_cart += item.quantity

        for item in items:
            total_cost_cart += item.get_total

    if total_item_cart==0:
        check = False
    else:
        check = True

    product_categories = ProductCategories.objects.all()

    context = {
        'total_item_cart' : total_item_cart,
        'product_categories': product_categories,
    }
    return render(request, 'store/cart.html', {'items' : items , 'context':context, 'total_cost_cart' : total_cost_cart, 'check':check})



def item_detail(request,id):

    total_item_cart = 0

    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

    product = Product.objects.get(id=id)

    product_categories = ProductCategories.objects.all()

    context = {
        'product_categories': product_categories,
        'total_item_cart' : total_item_cart,
    }

    return render(request,'store/item_detail.html',{'context': context, 'product' : product})



def order_details(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    total_item_cart = 0
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

    orders = FullOrder.objects.filter(user=request.user).order_by('-date_ordered')

    ordered = []
    for order in orders:
        tt = []
        items = Purchased_item.objects.filter(order=order)
        for item in items:
            tt.append(item)
        ordered.append({'order': order, 'items': tt})

    product_categories = ProductCategories.objects.all()
    
    context = {
        'product_categories': product_categories,
        'total_item_cart': total_item_cart,
    }
    return render(request,'store/order_details.html',{'context': context, 'ordered':ordered})



def make_payment(request,id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    dt = datetime.datetime.now()
    seq = int(dt.strftime("%Y%m%d%H%M%S"))

    adr = ShippingAddress.objects.get(id = id)
    obj = FullOrder.objects.create(user = request.user)

    obj.recepient_fullname = adr.recepient_fullname
    obj.phone_no = adr.phone_no
    obj.address_line1 = adr.address_line1
    obj.address_line2 = adr.address_line2
    obj.city = adr.city
    obj.state = adr.state
    obj.country = adr.country
    obj.zipcode = adr.zipcode
    try:
        obj.email = adr.email
    except:
        print("Please retry the email")
    obj.transaction_id = seq
    if (obj.transaction_id == seq):
        obj.success = True
    else:
        obj.success = False
    obj.save()

    total_amount = 0

    items = OrderItem.objects.all()
    for item in items:
        item_purchased = Purchased_item.objects.create(order = obj)
        item_purchased.user = request.user
        item_purchased.quantity = item.quantity
        item_purchased.name = item.product.name
        item_purchased.price = item.product.price
        item_purchased.image = item.product.image
        item_purchased.description = item.product.description
        item_purchased.save()
        total_amount += item.product.price * item.quantity

        item.delete()
    #import pdb;pdb.set_trace()
    obj.amount = total_amount
    obj.save()
    
    #trigger the observer.
    print("Observer Triggered")
    userOrder = ObserverPattern.UserOrderCore("Ordercore")
    orderObserver = ObserverPattern.OrderMonitoringCore()
    userOrder.attach(orderObserver)
    userOrder.user_id = id
    
    return render(request,'store/success.html')



def delete_address(request,id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    adr = ShippingAddress.objects.get(id=id)

    if adr.user != request.user:
        return Http404

    adr.delete()
    return HttpResponseRedirect(reverse('checkout'))


def show_items(request,id):
   # import pdb;pdb.set_trace()
    form = PrescriptionAddForm()
    total_item_cart = 0
    print(request)
    product_categories = ProductCategories.objects.all()
    if (id == SUN_CONST):
        temp_context = sunglassesDisp().get_product_context(id)
    if (id == LENS_CONST):
        temp_context = lensDisp().get_product_context(id)
    if (id == FRAMES_CONST):
        temp_context = framesDisp().get_product_context(id)
        check = framesDisp().post_prescription_details(request)
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity
    context = {
        'product_categories' : product_categories,
        'product_category' : temp_context['product_category'],
        'products': temp_context['products'],
        'total_item_cart': total_item_cart,
    }
    print(request)
    return render(request, 'store/show_items.html', {'form' : form, 'context': context})


def show_items_frames(request,id,shape=None):

    form = PrescriptionAddForm()
    total_item_cart = 0
    #print(id)
    #print("Called shpe",shape)
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

    product_category = ProductCategories.objects.get(id=id)

    temp_context = framesDisp().get_product_context_shape(id,shape)
    framesDisp().post_prescription_details(request)
    
    #temp_context['products'] = Product.objects.filter(category=product_category,shape=shape)
    
    #print("Product cat",product_category)
    product_categories = ProductCategories.objects.all()
    if(shape == 'noshape'):
        face_shape_text = 'No face identified in the uploaded image'
    else:
        face_shape_text = 'Your face shape is '+shape+', hence the recommended frames are:'
    context = {
        'product_categories' : product_categories,
        'product_category' : temp_context['product_category'],
        'products': temp_context['products'],
        'total_item_cart': total_item_cart,
    }
    return render(request, 'store/show_items.html', {'form' : form, 'context': context, 'text': face_shape_text})



def search(request):
    total_item_cart = 0

    query = request.GET['search']

    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

    product_categories = ProductCategories.objects.all()
    products_temp = Product.objects.all()

    products =[]

    for p in products_temp:
        if query.lower() in p.name.lower() or query.lower() in p.description.lower():
            products.append(p)

    context = {
        'product_categories': product_categories,
        'total_item_cart': total_item_cart,
    }

    return render(request, 'store/search.html', {'products' : products,'context':context})


def update_address(request,id):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    total_item_cart = 0
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity

    product_categories = ProductCategories.objects.all()

    adr = ShippingAddress.objects.get(id=id)

    if adr.user != request.user:
        return Http404()

    if request.method == 'POST':
        form = ShippingUpdateForm(request.POST,instance=adr)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('checkout'))
    else:
        form = ShippingUpdateForm(instance=adr)

    context = {
        'product_categories' : product_categories,
        'total_item_cart' : total_item_cart,
    }

    return render(request ,'store/update_address.html',{'context':context,'form' : form})

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

def success(request,id):

    print(id)
    mailinterm = sendEmail()
    mailinterm.sendmail(id)

    return render(request, 'store/success.html')

def face_image(request, id=None):
    
    total_item_cart = 0
    if request.user.is_authenticated:
        items = OrderItem.objects.filter(user=request.user)
        for item in items:
            total_item_cart += item.quantity
    product_categories = ProductCategories.objects.all()
    context = {
        'product_categories': product_categories,
        'total_item_cart': total_item_cart,
    }
    if request.method == 'POST': 
        form = FaceShapeForm(request.POST, request.FILES)

        if form.is_valid():
            
            image_get = form.save() 
            image_get.image = request.FILES['image']
            file_type = image_get.image.url
            #FaceShape.objects.get(form.cleaned_data.get("url"))
            file_url = STATIC_DIR + '/images' + file_type
            shape = face_shapes(file_url)
            print(shape)
            print(id)
            return redirect(show_items_frames, id=FRAMES_CONST, shape=shape)
            #return redirect(success) 
    else: 
        form = FaceShapeForm() 
    return render(request, 'store/face_upload.html', {'form' : form, 'context' : context}) 

def display_face(request): 
  
    if request.method == 'GET': 
  
        # getting all the objects of hotel. 
        Faces = FaceShape.objects.all()
        return render(request, 'store/show_face.html', {'show_face' : Faces})
  
def success(request): 
    return HttpResponse('successfully uploaded') 
