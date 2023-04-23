from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic as django_generic

from tags.models import Tag, TaggedItem
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

    tags = Tag.objects.all()
    selected_tag = request.GET.get('tag_id')

    if selected_tag:
        content_type = ContentType.objects.get_for_model(Product)
        tagged_item_ids = TaggedItem.objects.filter(tag_id=selected_tag, content_type=content_type).values_list(
            'object_id', flat=True)
        products = products.filter(id__in=tagged_item_ids)


    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    collections = Collection.objects.all()

    context = {
        'page': page,
        'collections': collections,
        'tags': tags,
        'selected_collection': collection_title,
        'selected_tag': selected_tag,
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
