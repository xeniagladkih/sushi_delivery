from .models import *
import json


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print('Cart:', cart)

    items = []
    order = {'get_cart_total':0, 'get_cart_items':0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]['quantity']

            menu_item = MenuItem.objects.get(id=i)
            total = (menu_item.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'id':menu_item.id,
                'menu_item': {
                    'id': menu_item.id,
                    'name': menu_item.name,
                    'price': menu_item.price,
                    'image': menu_item.image,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
        except:
            pass
    return {'cartItems': cartItems, 'order': order, 'items': items}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.ordermodel_set.all()
        cartItems = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        cartItems = cookie_data['cartItems']
        order = cookie_data['order']
        items = cookie_data['items']

    return {'cartItems':cartItems, 'order': order, 'items': items}


def guest_order(request, data):
    print('User is not logged in')

    print('COOKIES:', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        menu_item = MenuItem.objects.get(id=item['id'])

        order_model = OrderModel.objects.create(
            menu_item=menu_item,
            order=order,
            quantity=item['quantity']
        )
    return customer, order