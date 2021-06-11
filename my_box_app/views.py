from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .models import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'GET':
        return redirect('/')
    
    print(request.POST)

    errors = User.objects.basic_validator(request.POST)

    if errors:
        for error in errors.values():
            messages.error(request, error)
        return redirect('/')

        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        username = request.POST['username'],
        password = request.POST['password'],   

    else:   
        pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(
        first_name = request.POST['first_name'],
        last_name = request.POST['last_name'],
        username = request.POST['username'],
        password = pw,
         
        )
        request.session['user'] = new_user.first_name
        request.session ['user_id'] = new_user.id
        return redirect('/home')

def login(request):
    if request.method == "GET":
        return redirect('/')
    
    errors = User.objects.authenticate(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    user = User.objects.get(username=request.POST['username'])
    request.session['user'] = user.first_name
    request.session['user_id'] = user.id
    messages.success(request, "You successfully logged in!")
    return redirect('/home')
    


def home(request):
    if'user_id' not in request.session:
        return redirect('/')

    box = Box.objects.all().order_by("name") 
    users = User.objects.all()
    user = User.objects.get(id=request.session['user_id'])
    total_qty = sum(box.values_list('qty', flat=True))
    context = {
    "boxes": box,
    "all_user": users,
    "user": user,
    "total_qty": total_qty,
    }

    return render(request, "home.html", context)

def add_box(request):
    print(request.POST)

    errors = Box.objects.box_validator(request.POST)
    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/home')

        name = request.POST['name'],
        description = request.POST['decription'],
        qty = request.POST['qty'],
        location = request.POST['location'],
        note = request.POST['note'], 
        status = request.POST['status'],
    else:  
        add_box = Box.objects.create(
        name = request.POST['name'],
        description = request.POST['description'],
        qty = request.POST['qty'],
        location = request.POST['location'],
        note = request.POST['note'],
        status = request.POST['status'],
        user = User.objects.get(id=request.session['user_id'])
        
        )
        return redirect('/home')

def info(request,id):
    print(request.POST)

    user = User.objects.get(id=request.session['user_id'])
    box = Box.objects.get(id=id)
    boxes = Box.objects.all()
    users = User.objects.all()
    context = {
        'box': box,
        'boxes': boxes,
        "user": user,
        "users": users,
    }
    return render(request, 'info.html', context)


def search(request):
    print(request.POST)
    
    user = User.objects.get(id=request.session['user_id'])
    name = Box.objects.filter(name= request.POST['name'])
    location = Box.objects.filter(location = request.POST['location'])
    status = Box.objects.filter(status= request.POST['status'])
    location_qty = sum(location.values_list('qty', flat=True))
    name_qty = sum(name.values_list('qty', flat=True))
    context = {
        'user': user,
        'name': name,
        'location': location,
        'status': status,
        "name_qty": name_qty,
        "location_qty": location_qty,
    }

    return render(request, 'search.html', context)
  

def edit_user(request, user_id):
    print(request.POST)

    update_user = User.objects.get(id=user_id)
    
    update_user.first_name = request.POST['first_name']
    update_user.last_name = request.POST['last_name']
    update_user.username = request.POST['username']
    update_user.password = request.POST['password']
    update_user.save()
        
    return redirect('/home')

def edit_box(request, box_id):
    print(request.POST)

    update_box = Box.objects.get(id=box_id)

    update_box.user = User.objects.get(id=request.session['user_id'])
    update_box.name = request.POST['name']
    update_box.description = request.POST['description']
    update_box.qty = request.POST['qty']
    update_box.location = request.POST['location']
    update_box.note = request.POST['note']
    update_box.status = request.POST['status']
    update_box.save() 
        
    return redirect('/home')

def delete(request, user_id):
    print(request.POST)

    delete_user = User.objects.get(id=request.session['user_id'])
    delete_user.delete()

    return redirect('/')


def delete_box(request, box_id):
    print(request.POST)

    delete_box = Box.objects.get(id=box_id)
    delete_box.delete()

    return redirect('/home')

def profile(request,user_id):
    user = User.objects.get(id=request.session['user_id'])
    users = User.objects.all()
    boxes = Box.objects.all()
    context = {
        'user': user,
        'all_user': users,
        'boxes': boxes,
    }
    return render(request, 'profile.html', context)


def logout(request):
    request.session.clear()
    messages.success(request, "You have been logged out successfully!")
    return redirect('/')

def view(request):
    request.session.clear()
    messages.success(request, "Please log in to view account!")
    return redirect('/')

