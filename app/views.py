from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout
from django.contrib.auth.forms import PasswordChangeForm
import datetime, requests
from .forms import *
from .models import *

from MetschooInventory.settings import TELEGRAM_TOKEN, CHAT_ID

def telegram_notify(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    params = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        print("receiving new lend")
    else:
        print("Failed to send message. Error:", response.status_code)

# Create your views here.

@login_required
def home(request):
    return render(request,"pages/home.html")

def register(request):
    if request.method == "POST": 
        forms = RegistsForm(request.POST or None)
        if forms.is_valid():
            forms.save()
            return redirect("login")
    else:
        forms = RegistsForm()

    return render(request, "registration/register.html",{"form":forms})

def signin(request):
    if request.method == 'POST':
        forms = LoginForm(data=request.POST)
        if forms.is_valid():
            
            user = forms.get_user()
            login(request, user)
            return redirect('home') 
    else:
        forms = LoginForm()
        
    return render(request,"registration/login.html",{"form":forms})

@login_required
def logouts(request):
    if request.method == 'POST':
        logout(request)
        return redirect("login")

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request,"registration/password_change.html",{"form":form})

def reset_password(request):
    return render(request, "registration/password_reset_form.html")

def reset_password_confirm(request):
    return render(request, "registration/password_reset_confirm.html")

def reset_password_complete(request):
    return render(request, "registration/password_reset_complete.html")

def reset_password_done(request):
    return render(request, "registration/password_reset_done.html")

@login_required
def profile(request):
    if (request.method == "POST"):
        userprof = UpdateUserProfile(data=request.POST , instance=request.user)
        if userprof.is_valid():
            userprof.save()
            return redirect("profile")
    else:
        userprof = UpdateUserProfile(instance=request.user)
        
    return render(request,"pages/profile.html",{"editform":userprof})

@login_required
def category_detail(request, item_id):
    product = Barang.objects.get(id=item_id)
    if (request.method == "POST"):
        user = request.user.get_username()
        room = product.room
        id = product.id
        categories = product.category
        item = get_object_or_404(Barang, id=id)
        quantity = int(request.POST['quantity'])
        desc = request.POST['description']
        loan = Peminjaman(
                item_code=id,
                item=item, 
                client=get_object_or_404(Account, username=user),
                lending_quantity=quantity, 
                category=categories,
                room=room,
                description=desc,
                status="Diproses"
            )
        '''
        telegram_notify(
f"""
NAMA PEMINJAM                   : {user}
BARANG YANG INGIN DIPINJAM      : {product.name}
LOKASI/RUANGAN BARANG           : {room}
JUMLAH BARANG YANG DIPINJAM     : {quantity}
KATEGORI                        : {categories}
"""
            )'''
        loan.save()
        item.quantity -= quantity
        item.save()
        return redirect('lending')
    return render(request,"pages/category_detail.html",{"product":product})

@login_required
def category(request):
    if (request.method == "POST"):
        rooms = request.POST.get("room")
        categories=request.POST.get("category")
        display= Barang.objects.filter(room=rooms, category=categories)
        return render(request,"pages/category.html",{"Items":display})
    else:
        search = Barang.objects.filter()
        return render(request,"pages/category.html",{"Items":search})

@login_required
def lending(request):
    if request.method == "POST":
        id = request.POST["lend-code"]
        code = request.POST["item-code"]
        item = get_object_or_404(Barang, id=code)
        loan = Peminjaman.objects.get(pk=id)

        if "kembalikan" in request.POST:
            loan.status = "Dikembalikan"
            loan.return_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            loan.save()
            item.quantity += int(request.POST['quantity'])
            item.save()
            return redirect("history")
        
        if "batal" in request.POST:
            loan.status = "Dibatalkan"
            loan.return_time = None
            loan.save()
            item.quantity += int(request.POST['quantity'])
            item.save()
            return redirect("history")

    return render(request, "pages/lending.html", {"borrow":Peminjaman.objects.all()})

@login_required
def history(request):
    return render(request, "pages/history.html",context={"peminjaman":Peminjaman.objects.all()[::-1]})