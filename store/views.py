from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from cart.models import OrderItem
from django.http import HttpResponseForbidden
from customer.models import Notification

# Create your views here.
def product_register(request):
    if request.method == "POST":
        user_id = request.session.get('uid', None)  
        is_admin = request.session.get('admin', None)       
        if user_id or is_admin:  
            watchimage = request.FILES["watchimage"]
            watchname = request.POST.get("watchname")
            watchbrand = request.POST.get("watchbrand")
            watchprice = request.POST.get("watchprice")
            watchdescription = request.POST.get("watchdescription")
            stock_quantity = request.POST.get("stock_quantity")
            data = Product(userid=user_id if user_id else 'admin', watchimage=watchimage,watchname=watchname,watchbrand=watchbrand,watchprice=watchprice,watchdescription=watchdescription,stock_quantity=stock_quantity)
            data.save()
            additional_images = request.FILES.getlist('additional_images')
            for img in additional_images:
                ProductImage.objects.create(product=data, image=img)
            if user_id:  
                notification_message = f"Your product '{watchname}' has been successfully registered!"
                Notification.objects.create(notid=user_id, message=notification_message, is_read=False)
            if is_admin:  
                return redirect('product_view') 
            else:
                return redirect('bankdetail') 

    return render(request, 'product_register.html')




def product_view(request):
    selected_brand = request.GET.get('brand', None)  
    search_query = request.GET.get('search', '')  
    if request.session.get('admin', False):
        data = Product.objects.all()
    else:
        data = Product.objects.exclude(userid=request.session.get('uid', None))
    if selected_brand:
        data = data.filter(watchbrand=selected_brand)
    if search_query:
        data = data.filter(watchname__icontains=search_query) | data.filter(watchbrand__icontains=search_query)
    brands = Product.objects.values_list('watchbrand', flat=True).distinct()

    return render(request, 'product_view.html', {'productdata': data,'selected_brand': selected_brand,'search_query': search_query, 'brands': brands,})


def productdelete(request,id):
    data=Product.objects.get(pk=id)
    data.delete()
    return redirect(product_view)


def productupdate(request,id):
    data=Product.objects.get(pk=id)
    return render(request,'productupdate.html',{'result':data})

def productupdates(request, id):
    product = Product.objects.get(id=id)
    
    if request.method == "POST":
        watchimage = request.FILES.get('watchimage')
        watchname = request.POST.get("watchname")
        watchbrand = request.POST.get("watchbrand")
        watchprice = request.POST.get("watchprice")
        watchdescription = request.POST.get("watchdescription")
        stock_quantity = request.POST.get("stock_quantity")
        if watchimage:
            if product.watchimage:
                product.watchimage.delete()  
            product.watchimage = watchimage
        product.watchname = watchname
        product.watchbrand = watchbrand
        product.watchprice = watchprice
        product.watchdescription = watchdescription
        product.stock_quantity = stock_quantity
        product.save()
        additional_images = request.FILES.getlist('additional_images')
        if additional_images:
            for img in additional_images:
                ProductImage.objects.create(product=product, image=img)
        delete_image_id = request.POST.get('delete_image')
        if delete_image_id:
            image_to_delete = ProductImage.objects.filter(id=delete_image_id).first()
            if image_to_delete:
                image_to_delete.delete()
        if product.userid and product.userid != 'admin':
            notification_message = f"Your product '{product.watchname}' has been updated."
            Notification.objects.create(notid=product.userid, message=notification_message, is_read=False)

        return redirect('product_view')
    return render(request, 'productupdate.html', {'product': product})

def delete_additional_image(request, id, image_id):
    product = get_object_or_404(Product, id=id)
    image_to_delete = get_object_or_404(ProductImage, id=image_id, product=product)
    if request.method == "POST":
        image_to_delete.delete()
        return redirect('productupdate', id=id) 
    return render(request, 'confirm_delete_image.html', {'product': product, 'image': image_to_delete})



def user_products(request):
    userid=request.session['uid']
    data=Product.objects.filter(userid=userid)
    return render(request,'user_products.html',{'productdata':data})


def productdeleteu(request,id):
    data=Product.objects.get(pk=id)
    data.delete()
    return redirect(user_products)

def productupdateu(request,id):
    data=Product.objects.get(pk=id)
    return render(request,'productupdate_user.html',{'result':data})

def productupdate_user(request, id):
    userid = request.session.get('uid')  
    product = Product.objects.get(id=id, userid=userid)
    if request.method == "POST":
        if 'watchimage' in request.FILES:
            product.watchimage = request.FILES['watchimage']
        product.watchname = request.POST.get("watchname")
        product.watchbrand = request.POST.get("watchbrand")
        product.watchprice = request.POST.get("watchprice")
        product.watchdescription = request.POST.get("watchdescription")
        product.stock_quantity = request.POST.get("stock_quantity")
        additional_images = request.FILES.getlist('additional_images')
        if additional_images:
            for img in additional_images:
                ProductImage.objects.create(product=product, image=img)
        product.save()
        notification_message = f"Your product '{product.watchname}' has been updated."
        Notification.objects.create(notid=product.userid, message=notification_message, is_read=False)
        return redirect('user_products')
    return render(request, 'productupdate_user.html', {'product': product})


def product_detail(request, product_id):
    product = Product.objects.filter(id=product_id).first()
    additional_images = product.additional_images.all()  
    return render(request, 'product_detail.html', {'product': product, 'additional_images': additional_images})


