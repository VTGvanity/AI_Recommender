from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm  # Make sure to import your form!

def product_list(request):
    products = Product.objects.all()
    # Adding a dummy 'recommendations' list so your template doesn't crash on the recommendations loop
    return render(request, 'store/product_list.html', {'products': products, 'recommendations': []})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Send the user back to the list after saving
    else:
        form = ProductForm()
    
    return render(request, 'store/add_product.html', {'form': form})