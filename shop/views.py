from django.shortcuts import get_object_or_404, render, redirect
from .models import Category, Product, StaffRole
from cart.forms import FormToAddProduct
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here
def home(request):
    return render(request, 'shop/home.html')

# Custom decorator to restrict access to baristas only
def barista_required(view_func):
    """Custom decorator to restrict access to baristas only."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login page if not logged in
        if not StaffRole.objects.filter(user=request.user, name='Barista').exists():
            return redirect('shop:product_list')  # Redirect unauthorized users
        return view_func(request, *args, **kwargs)
    return wrapper

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

    # Adding to the cart the button 'Add to cart'
    cart_product_form = FormToAddProduct()
    return render(
        request,
        'shop/product/detail.html',
        {'product': product, 'cart_product_form': cart_product_form}
    )


