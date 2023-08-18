from models import Worker, get_image_list
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddApplicationForm
from django.conf import settings
import os

def home(request):
    workers = Worker.objects.all()

    if request.method == 'POST':  # post login form to backend
        username = request.POST['username']
        password = request.POST['password']
        # Login data auth
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in")
        else:
            messages.error(request, "Error logging in, check your Username and Password")

    image_list = get_image_list()  # Call the function to get the image URLs
    
    return render(request, 'home.html', {'workers': workers, 'image_list': image_list})
def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        print(request.POST)  # Print POST data for debugging
        print(request.FILES)  # Print uploaded files for debugging
        if form.is_valid():
            form.save()
            #auth + login post registration
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration Successful.")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})

def customer_application(request, pk):
    if request.user.is_authenticated:
        #look up application
        customer_application = Worker.objects.get(id=pk)
        return render(request, 'application.html', {'customer_application':customer_application})
    else:
        messages.success(request, "You must be logged in to view this page.")
        return redirect('home')
    
def delete_application(request, pk):
    if request.user.is_authenticated:
        delete_app = Worker.objects.get(id=pk)
        delete_app.delete()
        messages.success(request, "Application deleted")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete applications")
        return redirect('home')

def add_application(request):
    form = AddApplicationForm(request.POST or None, request.FILES or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_application = form.save()
                messages.success(request, "Application added")
                return redirect('home')
        return render(request, 'add_application.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to add applications")
        return redirect('home')
    
def update_application(request, pk):
    if request.user.is_authenticated:
        current_application = Worker.objects.get(id=pk)
        form = AddApplicationForm(request.POST or None, request.FILES or None, instance=current_application)
        if form.is_valid():
            form.save()
            messages.success(request, "Application updated")
            return redirect('home')
        return render(request, 'update_application.html', {'form':form})
    else:
        messages.success(request, "You must be logged in to update applications")
        return redirect('home')
    
def get_image_list():
    print("get_image_list() function is being called") 
    image_directory = os.path.join(settings.MEDIA_ROOT, 'images')
    image_list = []

    for filename in os.listdir(image_directory):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            image_url = os.path.join(settings.MEDIA_URL, 'images', filename)
            print(f"Image URL: {image_url}")  # Debug print
            image_list.append(image_url)

    return image_list
    
def your_view(request):
    image_list = get_image_list()
    # Your view logic here
    # Retrieve the list of image URLs (image_list)
    context = {
        'image_list': image_list,
    }
    return render(request, 'home.html', context)

