from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic as django_generic

from tags.models import Tag, TaggedItem
from .models import Product, Collection


def product_list(request):
    collection_title = request.GET.get('collection')
    search_query = request.GET.get('search', '')

    products = Product.objects.all() #get all the products from database

    if collection_title:
        products = products.filter(collection__title=collection_title) #used to display items in different categories/collections

    if search_query:
        products = products.filter(Q(title__icontains=search_query)) #used in the search function

    tags = Tag.objects.all() #get all tags from database
    selected_tag = request.GET.get('tag_id')

    #get all the products that match a specific tag
    if selected_tag:
        content_type = ContentType.objects.get_for_model(Product)
        tagged_item_ids = TaggedItem.objects.filter(tag_id=selected_tag, content_type=content_type).values_list(
            'object_id', flat=True)
        products = products.filter(id__in=tagged_item_ids)

    #display 10 items per page
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    collections = Collection.objects.all() #get all collections/categories

    context = {  #dictionary for displaying the product list
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
