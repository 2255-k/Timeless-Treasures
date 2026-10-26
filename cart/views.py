from django.shortcuts import render, redirect
from .models import CartZ,Payment,Order,OrderItem
from django.urls import reverse
from store.models import  Product
from customer.models import  UserDetails,Notification
from .models import  ShippingAddress
from .forms import ShippingAddressForm
import razorpay
from django.conf import settings

def add_to_cart(request):
    if 'uid' not in request.session:
        return redirect('user_login')  
    cuser = request.session['uid']  
    if request.method == "POST":
        cartimage = request.POST.get("cartimage")
        cartname = request.POST.get("cartname")
        cartbrand = request.POST.get("cartbrand")
        cartprice = request.POST.get("cartprice")
        cartdescription = request.POST.get("cartdescription")
        product = Product.objects.filter(watchname=cartname, watchbrand=cartbrand).first()
        if not product:
            return redirect('cart')  
        existing_cart_item = CartZ.objects.filter(cuser=cuser, cartname=cartname, cartbrand=cartbrand).first()
        if existing_cart_item:
            if product.stock_quantity > existing_cart_item.quantity:
                existing_cart_item.quantity += 1
                existing_cart_item.save()  
        else:
            if product.stock_quantity > 0:
                CartZ.objects.create(cuser=cuser,cartimage=cartimage,cartname=cartname,cartbrand=cartbrand,cartprice=cartprice,cartdescription=cartdescription,quantity=1 )

        cart_items_count = CartZ.objects.filter(cuser=cuser).count()
        request.session['cart_items_count'] = cart_items_count
        return redirect('cart') 
    return render(request, 'cart.html')  

def cart(request):
    cuser = request.session.get('uid')  
    if not cuser:
        return redirect('user_login')  

    data = CartZ.objects.filter(cuser=cuser)
    discount = 0
    discount_amount = 0

    if request.method == "POST":
        cart_id = request.POST.get('cart_id')
        if 'increase' in request.POST:
            cart_item = CartZ.objects.get(id=cart_id, cuser=cuser)
            product = Product.objects.filter(watchname=cart_item.cartname, watchbrand=cart_item.cartbrand).first()
            if product and cart_item.quantity + 1 <= product.stock_quantity:
                cart_item.quantity += 1
                cart_item.save()
        elif 'decrease' in request.POST:
            cart_item = CartZ.objects.get(id=cart_id, cuser=cuser)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
        elif 'delete' in request.POST:
            cart_item = CartZ.objects.get(id=cart_id, cuser=cuser)
            cart_item.delete()
        elif 'increase_by_7' in request.POST:
            cart_item = CartZ.objects.get(id=cart_id, cuser=cuser)
            product = Product.objects.filter(watchname=cart_item.cartname, watchbrand=cart_item.cartbrand).first()
            if product and cart_item.quantity + 7 <= product.stock_quantity:
                cart_item.quantity += 7
                cart_item.save()

        elif 'update_quantity' in request.POST:
            new_quantity = int(request.POST.get('quantity'))  
            cart_item = CartZ.objects.get(id=cart_id, cuser=cuser)
            product = Product.objects.filter(watchname=cart_item.cartname, watchbrand=cart_item.cartbrand).first()
            if product and 1 <= new_quantity <= product.stock_quantity: 
                cart_item.quantity = new_quantity
                cart_item.save()

        return redirect('cart')
    
    total_amount = 0
    for item in data:
        total_amount += float(item.cartprice) * item.quantity
        if item.quantity >= 7:  
            discount = 0.10
            discount_amount = total_amount * discount

    final_amount = total_amount - discount_amount
    for item in data:
        product = Product.objects.filter(watchname=item.cartname, watchbrand=item.cartbrand).first()
        if product:
            item.stock_quantity = product.stock_quantity
        else:
            item.stock_quantity = 0  

    return render(request, 'cart.html', {'cartdata': data,'total_amount': total_amount,'final_amount': final_amount,'discount_amount': discount_amount, })


def checkout(request):
    cuser = request.session.get('uid')
    if not cuser:
        return redirect('login')
    cart_items = CartZ.objects.filter(cuser=cuser)
    shipdata = ShippingAddress.objects.filter(user_details_id=cuser).first()
    total_inr = sum([float(item.cartprice) * item.quantity for item in cart_items])
    discount_amount = 0
    for item in cart_items:
        if item.quantity >= 7:
            discount = 0.10  # 10% discount
            discount_amount = total_inr * discount
            break 
    shipping_charge = 100
    total_inr_with_shipping = total_inr + shipping_charge 
    final_inr = total_inr_with_shipping - discount_amount
    total_amount = int(final_inr * 100)
    if request.method == "POST":
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            if shipdata:
                shipdata.delete()       
            shipping_address = form.save(commit=False)
            shipping_address.user_details_id = cuser  
            shipping_address.save()
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
            order = client.order.create({'amount': total_amount,'currency': 'INR','payment_capture': '1',}) 
            order_id = order['id']
            return render(request, 'payment.html', {'order_id': order_id,'total_inr': final_inr,'razorpay_key': settings.RAZORPAY_API_KEY,'discount_amount': discount_amount,'final_amount': final_inr,'shipping_charge': shipping_charge })
    else:
        form = ShippingAddressForm()
    return render(request, 'checkout.html', {'cart_items': cart_items,'shipdata': shipdata,'form': form,'total_inr': total_inr,'discount_amount': discount_amount,'final_inr': final_inr,'shipping_charge': shipping_charge})


def payment(request):
    user_id = request.session.get('uid')
    user_details = UserDetails.objects.get(id=user_id)
    cart_items = CartZ.objects.filter(cuser=user_id)
    total_amount = 0
    discount_amount = 0
    discount = 0
    shipping_charge = 100  
    for item in cart_items:
        total_amount += float(item.cartprice) * item.quantity
        if item.quantity >= 7:
            discount = 0.10
            discount_amount = total_amount * discount
            break
    final_amount = total_amount - discount_amount + shipping_charge
    total_amount_in_paise = int(final_amount * 100)
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    razorpay_order = client.order.create({'amount': total_amount_in_paise, 'currency': 'INR', 'payment_capture': '1'})
    payment = Payment.objects.create(user_id=user_id, amount=final_amount, razorpay_order_id=razorpay_order['id'],)
    return render(request, 'payment.html', {'cart_items': cart_items,'total_amount': total_amount,'final_amount': final_amount,'discount_amount': discount_amount,'shipping_charge': shipping_charge, 'order_id': razorpay_order['id'],'razorpay_key_id': settings.RAZORPAY_API_KEY,'user_id': user_id,})

def verify_payment(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('order_id')
        signature = request.POST.get('razorpay_signature')
        params_dict = {'razorpay_order_id': order_id,'razorpay_payment_id': payment_id,'razorpay_signature': signature}
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
        client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.filter(razorpay_order_id=order_id).first()
        if payment:
            payment.razorpay_payment_id = payment_id
            payment.paid = True
            payment.save()
            success_url = reverse('payment_success') + f'?order_id={order_id}&payment_id={payment_id}&success=True'
            return redirect(success_url)
        return render(request, 'payment_failed.html', {'error': 'Payment verification failed. Please try again.'})
    return render(request, 'payment_failed.html', {'error': 'Invalid request method.'})


def payment_success(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id') 
    
    if not payment_id or not order_id:
        message = 'Payment failed. Please try again.'
        return render(request, 'payment_success.html', {'message': message, 'success': False})
    client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
    order_details = client.order.fetch(order_id)  
    cuser = request.session.get('uid')  
    user_details = UserDetails.objects.get(id=cuser)  
    cart_items = CartZ.objects.filter(cuser=cuser)
    total_price = 0
    grouped_cart_items = {}
    for cart_item in cart_items:
        product_key = (cart_item.cartname, cart_item.cartbrand)
        if product_key not in grouped_cart_items:
            grouped_cart_items[product_key] = {'cartname': cart_item.cartname,'cartbrand': cart_item.cartbrand,'cartprice': cart_item.cartprice,'quantity': 0}
        grouped_cart_items[product_key]['quantity'] += cart_item.quantity
    for product_key, group in grouped_cart_items.items():
        cart_item_price = group['cartprice']
        total_price += cart_item_price * group['quantity']
    shipping_charge = 100
    discount_amount = 0  
    for item in cart_items:
        if item.quantity >= 7:
            discount_amount = total_price * 0.10
            break
    final_amount = total_price - discount_amount + shipping_charge
    total_amount_in_paise = int(final_amount * 100)  

    payment = Payment.objects.create(user_id=user_details.id,amount=order_details['amount'] / 100,   razorpay_order_id=order_id, razorpay_payment_id=payment_id, paid=True)
    order = Order.objects.create(user_id=user_details.id,total_price=total_price,  payment_id=payment.id,status='ORDER_PLACED' )
    if payment.paid:
        order.status = 'PROCESSING_ORDER'
        order.save()
    for product_key, group in grouped_cart_items.items():
        order_item = OrderItem(order_id=order.id,product_name=group['cartname'],product_brand=group['cartbrand'],product_price=group['cartprice'],product_quantity=group['quantity'],total_amount=group['cartprice'] * group['quantity'])
        order_item.save()
    for cart_item in cart_items:
        product = Product.objects.filter(watchname=cart_item.cartname, watchbrand=cart_item.cartbrand).first()
        if product and product.stock_quantity >= cart_item.quantity:
            product.stock_quantity -= cart_item.quantity
            product.save()  
        cart_item.delete()  
    notification_message = f"Thank you for purchasing! Your order {order.id} has been confirmed."
    Notification.objects.create(notid=user_details.id, message=notification_message, is_read=False)
    message = 'Payment was successful and your order is confirmed.'
    return render(request, 'payment_success.html', {'payment_id': payment.razorpay_payment_id,'order_id': order.id,'amount_paid': payment.amount,'payment_status': 'Paid','final_amount': final_amount,'total_amount_in_paise': total_amount_in_paise,'message': message,'success': True,'shipping_charge': shipping_charge,'discount_amount': discount_amount})



def payment_failed(request):
    error_message = request.GET.get('error', 'An unknown error occurred during payment.')
    order_id = request.GET.get('order_id')
    return render(request, 'payment_failed.html', {'error': error_message,'order_id': order_id})







