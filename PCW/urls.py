"""PCW URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings

from PCW.views import home, cart
from PCW.views import search
from PCW.views import cart_session
from PCW.views import get_cart
from PCW.views import cart_list
from PCW.views import delete_product
from PCW.views import register
from PCW.views import login
from PCW.views import sendCookies
from PCW.views import getCookies
from PCW.views import send_cookie_to_loginPage


urlpatterns = [
    path("", home, name="home"),
    path("register", register, name="register"),
    path("login", login, name="login"),
    path("search", search),
    path("admin/", admin.site.urls),
    path("send_to_cart", cart_session),
    path("get_cart", get_cart),
    path("cart", cart_list, name="cart"),
    path("delete_product", delete_product),
    path("sendCookies", sendCookies),
    path("getCookies", getCookies),
    path("send_cookie_to_loginPage", send_cookie_to_loginPage),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
