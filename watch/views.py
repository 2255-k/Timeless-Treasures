from django.shortcuts import render,redirect
from customer. models import UserDetails,bankdetailz,Notification
from store. models import Product
from cart.models import CartZ,OrderItem,Payment,Order,ShippingAddress

def index(request):
    is_admin = request.session.get('admin')
    user_id = request.session.get('uid')
    if user_id:
        unread_notifications_count = Notification.objects.filter(notid=user_id, is_read=False).count()
    else:
        unread_notifications_count = 0  
    if is_admin:
        product_data = Product.objects.all()
    else:
        product_data = Product.objects.exclude(userid=user_id)
    return render(request, 'index.html', {
        'productdata': product_data,
        'unread_notifications_count': unread_notifications_count  
    })

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')


def watches(request):
    return render(request,'watches.html')

def gallery(request):
    return render(request,'gallery.html')

def contact(request):
    return render(request,'contact.html')

def antique_watch_history(request):
    return render(request, 'antique_watch_history.html')

def termsofservice(request):
    return render(request, 'termsofservice.html')

def returnpolicy(request):
    return render(request, 'returnpolicy.html')


def shipping_page(request):
    return render(request,'shipping_page.html')


def login(request):
    return render(request,'user_login.html')


def login(request):
    useremail = request.POST.get('useremail')   
    userpassword = request.POST.get('userpassword')  
    if useremail == 'admin@gmail.com' and userpassword == 'admin':
        request.session['email'] = useremail
        request.session['admin'] = 'admin'
        return render(request, 'index.html', {'status': 'admin login success'})
    elif UserDetails.objects.filter(useremail=useremail, userpassword=userpassword).exists():
        userdetails = UserDetails.objects.get(useremail=useremail, userpassword=userpassword)      
        if userdetails.userpassword == userpassword:
            request.session['uid'] = userdetails.id
            request.session['uname'] = userdetails.username
            request.session['uemail'] = useremail
            request.session['user'] = 'user'
            Notification.objects.create(
                notid=userdetails.id,  
                message=f"Welcome back, {userdetails.username}!", is_read=False )
            unread_notifications_count = Notification.objects.filter(notid=userdetails.id, is_read=False).count()
            unread_notifications = Notification.objects.filter(notid=userdetails.id, is_read=False)
            return render(request, 'index.html', {'status': 'login success','unread_notifications_count': unread_notifications_count,'unread_notifications': unread_notifications  })
    else:
        return render(request, 'user_login.html', {'status': 'login failed'})
    
def logout(request):
   session_keys = list(request.session.keys())
   for key in session_keys:
          del request.session[key]
   return redirect(index)  


def user_view(request):
    userdata = UserDetails.objects.all() 
    bankdetails = bankdetailz.objects.all() 
    return render(request, 'user_view.html', {'userdata': userdata, 'bankdetails': bankdetails})


def userdelete(request, id):
    user_details = UserDetails.objects.get(pk=id)
    bankdetailz.objects.filter(bankuser=user_details.id).delete()
    user_details.delete()
    return render(request, 'user_view.html')
 

def userupdate(request,id):
    data=UserDetails.objects.get(pk=id)
    return render(request,'userupdate.html',{'result':data})

def userupdates(request,id):
    if request.method=="POST":
        username=request.POST.get("username")
        userphone=request.POST.get("userphone")
        useremail=request.POST.get("useremail")
        userpassword=request.POST.get("userpassword")
        data=UserDetails(id=id,username=username,userphone=userphone,useremail=useremail,userpassword=userpassword)
        data.save()
        return redirect('user_profile')
    return render(request,'userupdate.html')  


def terms_and_conditions(request):
    return render(request, 'terms_and_conditions.html')



def adminview_orders(request):
    orders = Order.objects.all().order_by('-order_date')  
    order_details = []

    for order in orders:
        shipping_address = ShippingAddress.objects.filter(user_details_id=order.user_id).first()
        payment = Payment.objects.filter(id=order.payment_id).first()  
        order_items = OrderItem.objects.filter(order_id=order.id)
        order_items_with_seller = []
        total_quantity = sum(item.product_quantity for item in order_items)
        discount_amount = 0.0
        if total_quantity > 7:
            discount_amount = float(order.total_price) * 0.1 
        final_price = float(order.total_price) - discount_amount  
        for item in order_items:
            product = Product.objects.filter(watchname=item.product_name).first()
            seller_name = seller_phone = seller_email = 'User not found'     
            if product and product.userid:
                seller_id_or_username = product.userid  
                if seller_id_or_username.isdigit():
                    seller = UserDetails.objects.filter(id=int(seller_id_or_username)).first()
                else:
                    seller = UserDetails.objects.filter(username=seller_id_or_username).first()
                
                if seller:
                    seller_name = seller.username
                    seller_phone = seller.userphone
                    seller_email = seller.useremail
                else:
                    seller_name = "Admin"
                    seller_phone = seller_email = None  
            
            individual_price = float(item.total_amount) / float(item.product_quantity) if item.product_quantity > 0 else 0.0
            order_items_with_seller.append({'product_name': item.product_name,'quantity': item.product_quantity,'total_price': float(item.total_amount),'individual_price': individual_price,'product_image': product.watchimage.url if product and product.watchimage else None,'seller_name': seller_name,'seller_phone': seller_phone,'seller_email': seller_email})
        order_details.append({'order': order,'shipping_address': shipping_address,'payment': payment,'order_items': order_items_with_seller,'total_quantity': total_quantity,'discount_amount': discount_amount,'final_price': final_price})

    return render(request, 'adminview_orders.html', {'order_details': order_details})


def useraddedproducts(request):
    products = Product.objects.filter(userid__isnull=False).exclude(userid='').order_by('-id')
    product_details = []
    for product in products:
        seller_name = seller_phone = seller_email = 'Owner'
        if product.userid:
            seller_id_or_username = product.userid
            if seller_id_or_username.isdigit():
                seller = UserDetails.objects.filter(id=int(seller_id_or_username)).first()
            else:
                seller = UserDetails.objects.filter(username=seller_id_or_username).first()
            if seller:
                seller_name = seller.username
                seller_phone = seller.userphone
                seller_email = seller.useremail
        product_details.append({'product_name': product.watchname,'product_image': product.watchimage.url if product.watchimage else None,'seller_name': seller_name,'seller_phone': seller_phone,'seller_email': seller_email,})

    return render(request, 'useraddedproducts.html', {'product_details': product_details})


def track_order(request):
    user_id = request.session.get('uid')  
    if not user_id:
        error_message = "You must be logged in to track orders."
        return render(request, 'track_order.html', {'error_message': error_message})
    orders = Order.objects.filter(user_id=user_id).order_by('-order_date')
    orders_with_items = []
    order_status_messages = {
        'ORDER_PLACED': "Your order has been placed.",
        'PROCESSING_ORDER': "Your order is being processed.",
        'QUALITY_CHECK': "Your order is under quality check.",
        'DISPATCHED': "Your order has been dispatched.",
        'SHIPPED': "Your order has been shipped.",
        'OUT_FOR_DELIVERY': "Your order is out for delivery.",
        'DELIVERED': "Your order has been delivered."
    }
    
    for order in orders:
        order_items = OrderItem.objects.filter(order_id=order.id)
        orders_with_items.append({
            'order': order,
            'order_items': order_items
        })

        for status, message in order_status_messages.items():
            if order.status == status and not Notification.objects.filter(
                    notid=user_id, message=f"Your order #{order.id}: {message}").exists():
                Notification.objects.create(
                    notid=user_id,
                    message=f"Your order #{order.id}: {message}",
                    is_read=False
                )
    if not orders_with_items:
        error_message = "You have not placed any orders yet."
        return render(request, 'track_order.html', {'error_message': error_message})
    return render(request, 'track_order.html', {'orders_with_items': orders_with_items})

def brand_index(request):
    brands = Product.objects.exclude(watchbrand__exact="").values('watchbrand').distinct()
    if not brands:
        brands = []
    return render(request, 'brand_index.html', {'brands': brands})

def seller_order_tracking(request):
    user_id = request.session.get('uid') 
    
    if not user_id:
        error_message = "You must be logged in to track orders."
        return render(request, 'track_order.html', {'error_message': error_message})
    seller_products = Product.objects.filter(userid=user_id)
    order_items = OrderItem.objects.filter(product_name__in=[p.watchname for p in seller_products])
    
    orders_with_items = []
    
    for item in order_items:
        order = Order.objects.filter(id=item.order_id).first()
        
        if order:
    
            if order.user_id != user_id:
             
                order_details = { 'order': order,'order_items': [item], 'order_status': order.status,}
                
                orders_with_items.append(order_details)
    if not orders_with_items:
        error_message = "No orders have been sold by you yet."
        return render(request, 'track_order.html', {'error_message': error_message})
    orders_with_items.sort(key=lambda x: x['order'].order_date, reverse=True)
    return render(request, 'track_order.html', {'orders_with_items': orders_with_items})

