from django.shortcuts import get_object_or_404, render
from .models import Category, Product

# Create your views here

# Code to display the list of all available products
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True) # add only available products to the view
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request, 'shop/product/list.html',
        {
            'category': category,
            'categories': categories,
            'products': products
        }
    )

# Code to retrieve and display a single product by id and slug
def product_detail(request, id, slug):
    product = get_object_or_404(
        Product, id=id, slug=slug, available=True
    )
    return render(
        request,
        'shop/product/detail.html',
        {'product': product}
    )
