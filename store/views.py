from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Product
def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'store/product_detail.html', {'product': product})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order, created = Order.objects.get_or_create(
        user=request.user,
        completed=False
    )

    item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    item.quantity += 1
    item.save()

    return redirect('cart')


@login_required
def cart(request):
    order, created = Order.objects.get_or_create(
        user=request.user,
        completed=False
    )

    items = order.orderitem_set.all()

    return render(request, 'store/cart.html', {
        'items': items
    })


@login_required
def checkout(request):
    order = Order.objects.get(user=request.user, completed=False)
    order.completed = True
    order.save()

    return render(request, 'store/checkout.html')


def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'store/register.html', {
        'form': form
    })