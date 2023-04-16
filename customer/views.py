from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .models import *

from .admin import MenuItemResource
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .uploadings import UploadingMenuItems
from .utils import cart_data, guest_order
 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .helper import send_reset_pw_mail

from rest_framework import generics, status, views, response
from . import serializers
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse

import json
import datetime


class Account(View):
    def get (self, request, *args, **kwargs):
        path = request.path_info.lstrip('/')
        active_tab = 'tab1'

        if path == 'account/edit-account/':
            active_tab = 'tab1'
        elif path == 'account/address/':
            active_tab = 'tab2'
        elif path == 'account/wishlist/':
            active_tab = 'tab3'
        elif path == 'account/orders/':
            active_tab = 'tab4'

        context = {'active_tab': active_tab}
        context.update(cart_data(request))

        return render(request, 'customer/account.html', context)


def sign_up(request):
    if request.method == 'POST':
        username = request.POST['login']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['againpassword']
        next_url = request.POST.get('next')

        print(username, email, password, confirm_password)

        if password != confirm_password:
            return HttpResponse("Passwords do not match")
        if username in list(User.objects.values_list('username', flat=True).distinct()):
            pass
        if email in list(User.objects.values_list('email', flat=True).distinct()):
            return HttpResponse("Email is already in use")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        customer = Customer.objects.create(user=user, name=username, email=email)
        customer.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'

        login(request, user)
        if next_url:
            return redirect(next_url)
        else:
            return redirect('index')

    return render(request, 'customer/popup-reg.html')
    

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next_url = request.POST.get('next')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('index')
        else:
            return HttpResponse("Email or password is incorrect")

    context = {}
    return render(request, 'customer/popup-login.html', context)


def logout_page(request):
    next_url = request.GET.get('next')
    logout(request)
    return redirect(next_url or 'index')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if not User.objects.filter(email=email).first():
            return HttpResponse("Signup error")
        
        user = User.objects.get(email=email)
        send_reset_pw_mail(user)
        return HttpResponse("We have just sent you an email with password reset instructions")

    return render(request, 'customer/popup-pw.html')


class PasswordReset(generics.GenericAPIView):

    serializer_class = serializers.EmailSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']

        if not User.objects.filter(email=email).first():
            return HttpResponse("Signup error")
        
        user = User.objects.get(email=email)
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        # http://127.0.0.1:8000/reset-password/<encoded_pk>/<token> 

        reset_url = reverse(
            'reset-password',
            kwargs={'encoded_pk': encoded_pk, 'token': token}
        )

        reset_url = f"127.0.0.1:8000{reset_url}"

        return response.Response(
            {
                "message":
                f"Your password reset link: {reset_url}"
            },
            status = status.HTTP_200_OK,
        )


class ResetPassword(generics.GenericAPIView):
    serializer_class = serializers.ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'kwargs': kwargs}
        )

        serializer.is_valid(raise_exception=True)

        return response.Response(
            {"message": "Password reset complete"},
            status = status.HTTP_200_OK,
        )


class Index(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'customer/index.html', cart_data(request))


class About(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'customer/about.html', cart_data(request))


class Menu(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'customer/menu.html', cart_data(request))\
        

class CategoryPage(View):
    def get(self, request, *args, **kwargs):
        path = request.path_info.lstrip('/')
        category = ''

        if path == 'category/rolls/':
            category = 'Rolls'
        elif path == 'category/sushi/':
            category = 'Sushi'
        elif path == 'category/sets/':
            category = 'Sets'
        elif path == 'category/snacks/':
            category = 'Appetizers'
        elif path == 'category/drinks/':
            category = 'Drinks'
        elif path == 'category/sauces/':
            category = 'Sauces'
        elif path == 'category/merch/':
            category = 'Merchandise'

        category_items = MenuItem.objects.filter(category__name=category)

        context = {
            'category': category,
            'category_items': category_items,
        }
        context.update(cart_data(request))

        return render(request, 'customer/category.html', context)
    

class CategorySearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        category_items = MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query) |
            Q(description__icontains=query)
        )

        context = {
            'category_items': category_items
        }
        context.update(cart_data(request))

        return render(request, 'customer/category.html', context)
    

class Cart(View):
    def get(self, request, *args, **kwargs):
        data = cart_data(request)
        order = data["order"]
        items = data["items"]

        context= {'items': items,'order': order}
        return render(request, 'customer/cart.html', context)
    
    
class Checkout(View):
    def get(self, request, *args, **kwargs):
        data = cart_data(request)
        order = data["order"]
        items = data["items"]

        context= {'items': items,'order': order}
         
        return render(request, 'customer/checkout.html', context)


def update_item(request):
        data = json.loads(request.body)
        print(data['action'])
        itemId = data['itemId']
        action = data['action']

        print('Action:', action)
        print('itemId:', itemId)

        customer = request.user.customer
        menu_item = MenuItem.objects.get(id=itemId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderModel.objects.get_or_create(order=order, menu_item=menu_item)

        if action == 'add':
            orderItem.quantity += 1
        elif action == 'remove':
            orderItem.quantity -= 1
        elif action == 'delete':
            orderItem.quantity = 0

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was added', safe=False)


def process_order(request):
    data = json.loads(request.body)

    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guest_order(request, data)

    total = data['form']['total']
    order.transaction_id = transaction_id
    
    if int(total) == int(order.get_cart_total):
        order.complete = True
    order.save()
        
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
    )

    return JsonResponse('Payment complete!', safe=False)


class Diagrams(View):
    def get (self, request, *args, **kwargs):
        # Categories:
        
        categories = list(Category.objects.values_list('name', flat=True).distinct())

        category_values = []

        for category in categories:
            category_values.append(MenuItem.objects.filter
                                   (category__name__contains=category).count())
            
        # Cities:
        
        cities = list(ShippingAddress.objects.values_list('city', flat=True).distinct())

        city_values = []

        for city in cities:
            city_values.append(ShippingAddress.objects.filter
                                   (city__contains=city).count())

        context = {
            'categories': categories,
            'category_values': category_values,
            'cities': cities,
            'city_values': city_values,
        }
        
        return render(request, 'customer/diagrams.html', context)


class Export(View):
    def get (self, request, *args, **kwargs):
        return render(request, 'customer/export.html')
    

def export_files(request, format):
    menu_items_resource = MenuItemResource()
    dataset = menu_items_resource.export()
    if format == 'xls':
        dataset_format = dataset.xls
    else:
        dataset_format = dataset.csv
    response = HttpResponse(dataset_format, content_type=f"text/{format}")
    response['Content-Disposition'] = f"attachment; filename=export.{format}"
    return response


class FileNotChosenException(Exception):
    pass

def import_files(request):
    try:
        if request.method == 'POST':
            file = request.FILES.get('file')
            if not file:
                raise FileNotChosenException("No file was chosen to upload!")
            elif not file.name.endswith('xls'):
                messages.info(request, 'Wrong Format!')
            else:
                uploading_file = UploadingMenuItems({"file": file})
                if uploading_file:
                    messages.success(request, "Uploaded Successfully!")
                else:
                    messages.error(request, "Invalid request!")
    except FileNotChosenException as e:
        messages.warning(request, str(e))
    except ValueError as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, str(e))

    return render(request, 'customer/import.html', locals())