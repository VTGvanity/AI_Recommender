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
            # Create the product object but don't save to DB yet
            product = form.save(commit=False)
            
            # Initialize OpenAI client using your environment variable
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            
            try:
                # Ask AI to generate 3 relevant tags
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful e-commerce assistant."},
                        {"role": "user", "content": f"Suggest 3 short tags for a product named '{product.name}' in the category '{product.category}'. Return only the tags separated by commas."}
                    ]
                )
                # Store the AI's response in the tags field
                product.tags = response.choices[0].message.content
            except Exception as e:
                print(f"AI Tagging failed: {e}")
                product.tags = "General"

            product.save() # Save to MongoDB Atlas [cite: 1091]
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})