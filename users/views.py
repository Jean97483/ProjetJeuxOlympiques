import qrcode
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthentificationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from io import BytesIO
from offres.models import Offre

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('accueil')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('accueil')
    
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def simulate_payment(request, offre_id):
    user = request.user
    offre = Offre.objects.get(id=offre_id)

    user.generate_purchase_key()

    final_key = user.get_final_key()

    #Génération du QRCode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(final_key)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image = buffer.getvalue()

    return HttpResponse(qr_image, Content_type="image/png")