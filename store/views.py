from django.shortcuts import render, redirect
from .models import Product
from .forms import ProductForm  # Make sure to import your form!
from openai import OpenAI 
import os

def product_list(request):
    products = Product.objects.all()
    # Adding a dummy 'recommendations' list so your template doesn't crash on the recommendations loop
    return render(request, 'store/product_list.html', {'products': products, 'recommendations': []})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            
            # 1. Get the key safely
            api_key = os.getenv("OPENAI_API_KEY")
            
            # 2. Add a 'Safety Net' so it doesn't crash if the AI fails
            try:
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"Suggest 3 short tags for {product.name}. Only tags, comma separated."}
                    ]
                )
                product.tags = response.choices[0].message.content
            except Exception as e:
                # If AI fails, just set a default tag instead of crashing the site
                print(f"AI Error: {e}")
                product.tags = "General"

            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})