"""order URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from customer.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', Index.as_view(), name='index'),
    path('about/', About.as_view(), name='about'),

    path('account/', Account.as_view(), name='account'),
    path('account/address/', Account.as_view(), name='account-address'),
    path('account/edit-account/', Account.as_view(), name='account-edit'),
    path('account/wishlist/', Account.as_view(), name='account-wishlist'),
    path('account/orders/', Account.as_view(), name='account-orders'),

    path('menu/', Menu.as_view(), name='menu'),

    path('category/', CategoryPage.as_view(), name='category'),
    path('category/search/', CategorySearch.as_view(), name='category-search'),
    
    path('category/rolls/', CategoryPage.as_view(), name='category-rolls'),
    path('category/sushi/', CategoryPage.as_view(), name='category-sushi'),
    path('category/sets/', CategoryPage.as_view(), name='category-sets'),
    path('category/snacks/', CategoryPage.as_view(), name='category-snacks'),
    path('category/drinks/', CategoryPage.as_view(), name='category-drinks'),
    path('category/sauces/', CategoryPage.as_view(), name='category-sauces'),
    path('category/merch/', CategoryPage.as_view(), name='category-merch'),

    path('checkout/', Checkout.as_view(), name='checkout'),
    path('update_item/', update_item, name='update_item'),
    path('process_order/', process_order, name='process_order'),
    
    path('diagrams/', Diagrams.as_view(), name='diagrams'),

    path('export/', Export.as_view(), name='main'),
    path('export/<str:format>/', export_files, name='export'),

    path('import/', import_files, name='import'),

    path('sign_up/', sign_up, name='sign_up'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('reset-pw/', reset_password, name='reset-pw'),

    path('reset-password/', PasswordReset.as_view(), name='reset-password'),
    path('reset-password/<str:encoded_pk>/<str:token>/', ResetPassword.as_view(), name='reset-password'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
