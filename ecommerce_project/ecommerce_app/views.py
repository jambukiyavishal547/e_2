# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from .models import Product, Review
from .forms import ProductForm, ReviewForm
from django.db.models import Count
def index(request):
    # Sign in logic
    return render(request, 'index.html')

def signin(request):
    # Sign in logic
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')  # Redirect to product list page after signin
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signup(request):
    # Sign up logic
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')  # Redirect to signin page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('signin')  # Redirect to signin page after signout

def product_list(request):
    products = Product.objects.all()
    review_count=Product.objects.annotate(num_reviews=Count('review'))
    return render(request, 'product_list.html', {'products': products,'review_count':review_count})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list page after adding product
        else:
            form=form.errors
            print(form)
            msg="somthing wrong"
            return render(request, 'add_product.html',{'msg':msg})
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def edit_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list page after editing product
        else:
            form=form.errors
            print(form)
            msg="somthing wrong"
            return render(request, 'add_product.html',{'msg':msg})
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_product.html', {'form': form, 'product': product})

def add_review(request, pk):
    product = get_object_or_404(Product, id=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user  # Assuming you have user authentication
            review.save()
            return redirect('product_list')  # Redirect to product list page after adding review
    else:
        form = ReviewForm()
    return render(request, 'add_review.html', {'form': form, 'product': product})

