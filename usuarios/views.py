from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CriaUsuariosForm, CriaEmpresaForm, MudaUsuarioForm


def home(request):
    return render(request, 'home.html')


def Registrar(request):
    if request.method == 'POST':
        form = CriaUsuariosForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request,
                                username=username,
                                password=raw_password)
            # login(request, user)
            return redirect('home')
    else:
        form = CriaUsuariosForm()
    return render(request, 'register.html', {'form': form})


def RegistrarEmpresa(request):
    if request.method == 'POST':
        form = CriaEmpresaForm(request.POST)
        if form.is_valid():
            form.instance.is_empresa = True
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request,
                                username=username,
                                password=raw_password)
            # login(request, user)
            return redirect('home')
    else:
        form = CriaEmpresaForm()
    return render(request, 'register.html', {'form': form})
