from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from bank.models import BankAccount, Cashing, Deposit
from transactions.models import Expense, Revenue


# Create your views here.
def index(request):
    bank = BankAccount.objects.get(owner=request.user)
    cashing = Cashing.objects.filter(user=request.user)
    deposits = Deposit.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    revenues = Revenue.objects.filter(user=request.user)
    return render(request, 'core/index.html', {
        'bank': bank,
        'cashing': cashing,
        'deposits': deposits,
        'expenses': expenses,
        'revenues': revenues,
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, authenticated_user)
            return redirect('core:index')
        else:
            return render(request, 'core/login.html', {'login_form':form})
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'login_form':form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:index'))


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        context = {'form':form}
        if form.is_valid():
            form.save()
            return redirect('core:index')
        else:
            if form.errors:
                return render(request,'core/register.html', context)
    else:
        form = UserCreationForm()
        context = {'form':form}
        return render(request, 'core/register.html', context)
