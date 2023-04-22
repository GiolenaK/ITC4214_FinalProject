from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render

from .models import Product


def home(request):
    return HttpResponse('<h1>home</h1>')


def ShowAllProducts(request):
    products = Product.objects.order_by('-price').filter(is_published=True)

    page_num = request.GET.get("page")

    paginator = Paginator(products, 3)

    try:
        products = paginator.page(page_num)

    except PageNotAnInteger:

        products = paginator.page(1)

    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context= {
        'products': products
    }

    return render(request,'showProducts.html', context)
