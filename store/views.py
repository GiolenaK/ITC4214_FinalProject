from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic as django_generic
from .models import Product, Collection


def home(request):
    return HttpResponse('<h1>home</h1>')


def store_home(request):
    return render(request, 'store/home.html', {'title': 'Home'})


def store_about(request):
    return render(request, 'store/about.html', {'title': 'About'})


def product_list(request):
    collection_title = request.GET.get('collection')
    search_query = request.GET.get('search', '')

    products = Product.objects.all()

    if collection_title:
        products = products.filter(collection__title=collection_title)

    if search_query:
        products = products.filter(Q(title__icontains=search_query))

    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    collections = Collection.objects.all()

    context = {
        'products': products,
        'collections': collections,
        'selected_collection': collection_title
    }
    return render(request, 'store/product_list.html', context)


class ProductListView(django_generic.ListView):
    model = Product
    template_name = 'store/product_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        collection_id = self.request.GET.get('collection_id')
        if collection_id:
            queryset = queryset.filter(collection_id=collection_id)
        return queryset

class CollectionListView(django_generic.ListView):
    model = Collection
    template_name = 'store/collection_list.html'

