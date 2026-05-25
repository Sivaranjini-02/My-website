from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Product,Offer
from django.contrib.auth.forms import UserCreationForm

def index(request):
    products = Product.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'index.html', {'products': products, 'cart_count': cart_count})

def add_to_cart(request, product_id):
    if request.method == "POST":
        if 'cart' not in request.session:
            request.session['cart'] = {}
        cart = request.session['cart']
        product_id_str = str(product_id)
        cart[product_id_str] = cart.get(product_id_str, 0) + 1
        request.session.modified = True
        return JsonResponse({'success': True, 'total_items': sum(cart.values())})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def update_cart_quantity(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        action = request.POST.get('action')
        if product_id_str in cart:
            if action == 'increment':
                cart[product_id_str] += 1
            elif action == 'decrement':
                cart[product_id_str] -= 1
                if cart[product_id_str] <= 0:
                    del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('view_cart') # 7. Uses dynamic named routing

def remove_from_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_id_str = str(product_id)
        if product_id_str in cart:
            del cart[product_id_str]
        request.session['cart'] = cart
        request.session.modified = True
    return redirect('view_cart') # 7. Uses dynamic named routing

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    grand_total = 0
    for product_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))
        actual_price = product.discounted_price
        total_price = actual_price * quantity
        grand_total += total_price
        cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_price})
    return render(request, 'cart.html', {'cart_items': cart_items, 'grand_total': grand_total})


def home(request):
    featured_products = Product.objects.all()[:3]
    active_offers = Offer.objects.all()

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    context = {
        'featured_products': featured_products,
        'active_offers': active_offers,
        'cart_count': cart_count
    }
    return render(request, 'home.html', context)



def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem



@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('index')

    cart_items = []
    grand_total = 0
    for product_id_str, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id_str))
        total_price = product.discounted_price * quantity
        grand_total += total_price
        cart_items.append({'product': product, 'quantity': quantity, 'total_price': total_price})

    if request.method == "POST":
        address = request.POST.get('shipping_address')
        if address:

            order = Order.objects.create(user=request.user, shipping_address=address, total_amount=grand_total)


            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].discounted_price,
                    quantity=item['quantity']
                )

                item['product'].stock -= item['quantity']
                item['product'].save()


            request.session['cart'] = {}
            return render(request, 'checkout_success.html', {'order': order})

    return render(request, 'checkout.html', {'cart_items': cart_items, 'grand_total': grand_total})



def api_product_list(request):
    products = Product.objects.all()
    data = []
    for p in products:
        data.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'stock': p.stock
        })
    return JsonResponse({'products': data})

@login_required
def order_tracking(request):

    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_tracking.html', {'orders': user_orders})