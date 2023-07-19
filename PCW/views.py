import pprint

import requests
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json, asyncio, time, re
from asgiref.sync import sync_to_async
from .utiles import Utiles
from .utiles import Verify
from .utiles import Global

from priceComparison import main


def home(request):
    return render(request, "home.html")


def test():
    content = "Hello"
    return content

def compare(request):
    return render(request, "compare.html")

async def search(request):
    if request.method == 'GET':
        search_word = request.GET
        search_word = search_word["keyword"]
        cookies_response = cookies_product(request, search_word)
        print(cookies_response)
        print(search_word)
        # data = test()
        # data = await sync_to_async(main.activate, thread_sensitive=True)(search_word=search_word)
        ZipData = {}
        PrecisionData = {}
        AllData = {}

        try:
            data = main.activate(search_word)
            # pprint.pprint(data)
            ZipData = json.dumps(list(data["ZipData"]))
            PrecisionData = json.dumps(list(data["PrecisionData"]))
            AllData = json.dumps(list(data["AllData"]))
            pprint.pprint(json.loads(ZipData))
            # pprint.pprint(json.loads(PrecisionData))
            # pprint.pprint(json.loads(AllData))
        except Exception as e:
            print(e)

        # 直接建構HttpResponse物件
        # response = HttpResponse(content_type="application/json")
        # 會硬查詢後的資料Json, String
        # response.write("<h1>You had search {keyword}</h1>")
        # time.sleep(10)
    # return HttpResponse(data)
    return JsonResponse([ZipData, PrecisionData, AllData], safe=False)


cart = []

def cart_session(request):
    try:
        request.method = "GET"
        product_package = request.GET
        request.session["cart"] = product_package
        cart.append(request.session["cart"])
        print(product_package["product"])
    except Exception as e:
        print(e)

    return JsonResponse(data=cart, safe=False)


def get_cart(request):
    try:
        if request.method == "GET":
            print(cart)
            return JsonResponse([cart], safe=False)
        else:
            return render(request, "error.html")

    except Exception as e:
        print("Error", e)
        return render(request, "error.html", context=e)


def cart_list(request):
    return render(request, "cart.html")


def delete_product(request):
    try:
        if request.method == "GET":
            index = request.GET
            index = int(index["index"])
            cart.pop(index)
            return JsonResponse(cart, safe=False)
        else:
            return render(request, "error.html")

    except Exception as e:
        print("Error", e)
        return render(request, "error.html", context={"error": e})


def register(request):
    try:
        # receive POST request, queryDict object
        if request.method == "POST":
            # For filter WebKitFormBoundary POST request string
            if "{" in request.body.decode('utf-8'):
                response = request.body.decode('utf-8')  # response is a string
                response = json.loads(response)  # response is a json object(dict)
                print(response)

                Mysql = Utiles(response)
                Mysql.mysql()

                first_name = response["firstname"]
                last_name = response["lastname"]
                user_name = response["username"]
                email = response["email"]
                password = response["password"]
                confirm_password = response["confirmPassword"]

                return render(request, "register.html")

    except Exception as e:
        print("Error", e)
        return render(request, "error.html", context=e)

    return render(request, "register.html")


# Send Cookies
def sendCookies(request):
    print("Send Cookies")
    response = HttpResponse(content_type='text/plain')
    response.set_cookie(key='.credit', value='verified', httponly=True, expires=3600)  # 3600s = 1hr
    return response


def send_cookie_to_loginPage(request):
    try:
        credit = request.COOKIES['.credit']
        return JsonResponse(data=credit, safe=False)
    except:
        return JsonResponse(data="No Cookie, Please Login Again", safe=False)


def login(request):
    if request.method == "POST":
        response = request.body.decode('utf-8')
        response = json.loads(response)  # to convert string to json object

        result = Verify(response).verify()

        if result:
            print("Login Success")
            cookie_response = sendCookies(request)
            send_cookie_to_loginPage(request)
            Global.signIn = True

            return cookie_response

    return render(request, "login.html")


# Get Cookies
def getCookies(request):
    # credit = request.COOKIES['.credit']
    # print(f"credit: {credit}")
    # return JsonResponse(data=credit, safe=False)
    try:
        if request.method == "GET":
            credit = request.COOKIES['.credit']
            print(f"credit: {credit}")
            return JsonResponse(data=credit, safe=False)
        else:
            return render(request, "error.html")
    except:
        return JsonResponse(data="No Cookie, Please Login Again", safe=False)


def cookies_product(request, product):
    response = HttpResponse(content_type='text/plain')
    print(f"Send Cookies: {product}")
    response.set_cookie(key=".product", value=product, httponly=True, expires=3600)
    return response

def get_cookies_product(request):
    try:
        if request.method == "GET":
            product = request.COOKIES['.product']
            print(f"product: {product}")
            return JsonResponse(data=product, safe=False)
        else:
            return render(request, "error.html")
    except:
        return JsonResponse(data="No Cookie", safe=False)




