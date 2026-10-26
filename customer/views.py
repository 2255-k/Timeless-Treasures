from django.shortcuts import render,redirect
from . models import UserDetails ,bankdetailz,Notification
from cart . models import ShippingAddress ,Order,Payment,OrderItem,CartZ
from cart. forms import ShippingAddressForm
from store.models import Product


# Create your views here.

def user_register(request):
    if request.method=="POST":
      username=request.POST.get("username")
      userphone=request.POST.get("userphone")
      useremail=request.POST.get("useremail")
      userpassword=request.POST.get("userpassword")
      data=UserDetails(username=username,userphone=userphone,useremail=useremail,userpassword=userpassword)
      data.save()
      return redirect('user_login')
    return render(request,'user_register.html')


def user_profile(request):
    bankuser = request.session.get('uid')
    data = UserDetails.objects.filter(pk=bankuser).first()  
    if not data:
        return render(request, 'user_profile.html', {'message': "User not found!"})
    shipdata = ShippingAddress.objects.filter(user_details_id=bankuser).first()
    bankdata = bankdetailz.objects.filter(bankuser=bankuser).first()
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            new_shipping_address = form.save(commit=False)
            new_shipping_address.user_details_id = bankuser  
            new_shipping_address.save()
            return redirect('user_profile')  
    else:
        form = ShippingAddressForm() 
    return render(request, 'user_profile.html', {'result': data,'shipdata': shipdata,'bankdata': bankdata, 'form': form,   })

def order_summary(request):
    user_id = request.session.get('uid')
    orders = Order.objects.filter(user_id=user_id).order_by('-order_date')
    order_data = []

    for order in orders:
        payment = Payment.objects.filter(id=order.payment_id).first() if order.payment_id else None
        order_items = OrderItem.objects.filter(order_id=order.id)
        payment_status = 'Pending'
        payment_amount = 0
        razorpay_order_id = ''
        razorpay_payment_id = ''
        if payment:
            payment_status = 'Paid' if payment.paid else 'Pending'
            payment_amount = payment.amount
            razorpay_order_id = payment.razorpay_order_id
            razorpay_payment_id = payment.razorpay_payment_id
        shipping_charge = 100
        discount_amount = 0.0
        for item in order_items:
            if item.product_quantity >= 7:
                discount_amount += float(item.total_amount) * 0.1  
        final_amount = float(order.total_price) - discount_amount + shipping_charge
        total_amount_in_paise = int(final_amount * 100)
        has_large_quantity_item = any(item.product_quantity >= 7 for item in order_items)
        order_items_with_images = []
        for item in order_items:
            product = Product.objects.filter(watchname=item.product_name).first()
            product_image = product.watchimage.url if product and product.watchimage else None
            
            order_items_with_images.append({'product_name': item.product_name,'product_image': product_image,'product_quantity': item.product_quantity,'total_amount': item.total_amount,'product_id': item.id})
        
        order_data.append({'order_id': order.id,'total_price': float(order.total_price),'discount_amount': discount_amount,'shipping_charge': shipping_charge,  'payment_status': payment_status,'payment_amount': payment_amount,'razorpay_order_id': razorpay_order_id,'razorpay_payment_id': razorpay_payment_id,'order_items': order_items_with_images,'final_amount': final_amount,'total_amount_in_paise': total_amount_in_paise,'has_large_quantity_item': has_large_quantity_item})
    return render(request, 'order_summary.html', {'orders': order_data})

def bankdetail(request):
    bankuser = request.session.get('uid') 
    bankdata = bankdetailz.objects.filter(bankuser=bankuser).first()
    if bankdata:
        return redirect('user_products')
    if request.method == "POST":
        holdername = request.POST.get("holdername")
        accountno = request.POST.get("accountno")
        ifsc = request.POST.get("ifsc")
        data = bankdetailz(holdername=holdername, accountno=accountno, ifsc=ifsc, bankuser=bankuser)
        data.save() 
        return redirect('user_products')
    return render(request, 'bankdetail.html', {'bankdata': bankdata})
 


def view_notifications(request):
    user_id = request.session.get('uid')
    if request.method == "POST" and "clear_notifications" in request.POST:
        if user_id:
            Notification.objects.filter(notid=user_id).delete()  
        return redirect('view_notifications')  
    if user_id:
        notifications = Notification.objects.filter(notid=user_id).order_by('-date')
        Notification.objects.filter(notid=user_id, is_read=False).update(is_read=True)
    else:
        notifications = []
    return render(request, 'notifications.html', {'notifications': notifications})


def mark_notifications_read(request):
    user_id = request.session.get('uid')
    if user_id:
        Notification.objects.filter(notid=user_id, is_read=False).update(is_read=True)
    return redirect('view_notifications')  

def edit_shipping_address(request):
    cuser = request.session.get('uid')
    shipdata = ShippingAddress.objects.filter(user_details_id=cuser).first()
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipdata)
        if form.is_valid():
            form.save()
            return redirect('user_profile')  
    else:
        form = ShippingAddressForm(instance=shipdata)
    return render(request, 'edit_shipping_address.html', {'form': form})

def checkedit_shipping_address(request):
    cuser = request.session.get('uid')
    shipdata = ShippingAddress.objects.filter(user_details_id=cuser).first()
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST, instance=shipdata)
        if form.is_valid():
            form.save()
            return redirect('checkout')  
    else:
        form = ShippingAddressForm(instance=shipdata)
    return render(request, 'checkedit_shipping_address.html', {'form': form})

def view_order(request):
    user_id = request.session.get('uid')  
    latest_order = Order.objects.filter(user_id=user_id).order_by('-order_date').first()
    payment = Payment.objects.filter(id=latest_order.payment_id).first() if latest_order else None
    order_items = OrderItem.objects.filter(order_id=latest_order.id) if latest_order else []
    shipdata = ShippingAddress.objects.filter(user_details_id=user_id).first()
    order_items_with_images = []
    shipping_charge = 100
    discount_amount = 0  
    total_price = latest_order.total_price if latest_order else 0
    final_amount = total_price - discount_amount + shipping_charge  # 
    total_amount_in_paise = int(final_amount * 100) 

    for item in order_items:
        product = Product.objects.filter(watchname=item.product_name).first()
        product_image = product.watchimage.url if product and product.watchimage else None
        order_items_with_images.append({'product_name': item.product_name,'product_image': product_image,'quantity': item.product_quantity,'total_amount': item.total_amount,'product_id': item.id,})

    order_data = {'order_id': latest_order.id if latest_order else None,'total_price': total_price,'discount_amount': discount_amount,'shipping_charge': shipping_charge,  'final_amount': final_amount,'status': latest_order.status if latest_order else '','payment_status': 'Paid' if payment and payment.paid else 'Pending','payment_amount': payment.amount if payment else 0,'razorpay_payment_id': payment.razorpay_payment_id if payment else '','razorpay_order_id': payment.razorpay_order_id if payment else '','order_items': order_items_with_images,'shipping_address': shipdata}
    return render(request, 'view_order.html', {'order': order_data})


def products_bought_by_others(request):
    user_id = request.session.get('uid')
    seller_products = Product.objects.filter(userid=user_id)
    order_items = OrderItem.objects.filter(product_name__in=[p.watchname for p in seller_products])
    bought_by_others = []

    for item in order_items:
        order = Order.objects.filter(id=item.order_id).first()
        if order and order.user_id != user_id:  # Ensure the order belongs to someone else
            buyer = UserDetails.objects.filter(id=order.user_id).first()
            shipping_address = ShippingAddress.objects.filter(user_details_id=buyer.id).first()
            product = Product.objects.filter(watchname=item.product_name).first()
            product_image = product.watchimage.url if product and product.watchimage else None
            address = shipping_address.address if shipping_address else 'Address not available'
            city = shipping_address.city if shipping_address else ''
            postal_code = shipping_address.postal_code if shipping_address else ''
            country = shipping_address.country if shipping_address else ''
            full_address = f"{address}, {city}, {postal_code}, {country}"
            # Find the seller details
            seller = UserDetails.objects.filter(id=product.userid).first() if isinstance(product.userid, int) else UserDetails.objects.filter(username=product.userid).first()
            seller_name = seller.username if seller else 'Unknown Seller'
            notification_message_seller = f"Your product '{item.product_name}' has been bought by {buyer.username}."
            if not Notification.objects.filter(notid=user_id, message=notification_message_seller).exists():
                Notification.objects.create(notid=user_id, message=notification_message_seller)
            if order.status == 'DELIVERED':
                admin_message = "Admin has paid your amount successfully."
                if not Notification.objects.filter(notid=user_id, message=admin_message).exists():
                    Notification.objects.create(notid=user_id, message=admin_message)

            bought_by_others.append({
                'product_name': item.product_name,'buyer_name': buyer.username if buyer else 'Unknown','buyer_phone': buyer.userphone if buyer else 'Phone not available',  'buyer_email': buyer.useremail if buyer else 'Email not available','quantity': item.product_quantity,'total_price': item.total_amount,'order_date': order.order_date if order else 'Unknown','product_id': item.id,'admin_message': admin_message if order.status == 'DELIVERED' else "Admin will send you money within 24 hours.",'product_image': product_image,'shipping_address': full_address})
    bought_by_others = sorted(bought_by_others, key=lambda x: x['order_date'], reverse=True)
    return render(request, 'products_bought_by_others.html', {'bought_by_others': bought_by_others})



def userprofiledelete(request):
    if not request.session.get('uid'): 
        return redirect('user_login')  
    user_id = request.session['uid']
    user = UserDetails.objects.get(pk=user_id)
    bankdetailz.objects.filter(bankuser=user.pk).delete()  
    Product.objects.filter(userid=user.pk).delete()  
    CartZ.objects.filter(cuser=user.pk).delete()  
    user.delete()
    request.session.flush()  
    return redirect('index') 