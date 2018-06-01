from django.contrib import messages
from django.contrib.auth import authenticate ,login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from core.forms import BankAccountCreateForm
from core.models import Category, Tag
from bank.models import BankAccount
from transactions.models import Expense, Revenue
from transactions.forms import ExpenseEditForm, ExpenseMultipleEditForm, ExpenseForm, RevenueEditForm, RevenueForm


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        accounts = BankAccount.objects.filter(owner=request.user)
        expenses = Expense.objects.filter(user=request.user).order_by('due_date')
        revenues = Revenue.objects.filter(user=request.user).order_by('due_date')
        expense_categories = Category.objects.filter(expenses__user=request.user).distinct()
        revenue_categories = Category.objects.filter(revenues__user=request.user).distinct()

        return render(request, 'core/index.html', {
            'accounts': accounts,
            'expenses': expenses,
            'revenues': revenues,
            'expense_categories': expense_categories,
            'revenue_categories': revenue_categories,
        })
    return render(request, 'core/index.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, authenticated_user)
            messages.add_message(request, messages.SUCCESS, 'Olá, {}, seu login foi efetuado com sucesso'.format(request.user))
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
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('core:index')
        else:
            if form.errors:
                return render(request,'core/register.html', context)
    else:
        form = UserCreationForm()
        context = {'form':form}
        return render(request, 'core/register.html', context)


def expenses(request):
    categories = Category.objects.filter(owner=request.user)
    expenses = Expense.objects.filter(user=request.user)
    tags = Tag.objects.filter(owner=request.user)

    # FIXME: It's just for testing
    if request.method == 'POST':
        forms = [ExpenseMultipleEditForm(prefix=str(expense.title), instance=expense, data=request.POST) for expense in expenses]
        for form in forms:
            if form.is_valid():
                expense = form.save()
    else:
        forms = [ExpenseMultipleEditForm(prefix=str(expense.title), instance=expense) for expense in expenses]

    return render(request, 'core/expenses.html', {
        'expenses': expenses,
        'categories': categories,
        'tags': tags,
        'forms': forms,
    })


def revenues(request):
    categories = Category.objects.filter(owner=request.user)
    revenues = Revenue.objects.filter(user=request.user)
    tags = Tag.objects.filter(owner=request.user)
    return render(request, 'core/revenues.html', {
        'revenues': revenues,
        'categories': categories,
        'tags': tags,
    })


def expenses_edit(request, expense_id):
    expense = get_object_or_404(
        Expense.objects.filter(user=request.user).filter(id=expense_id)
    )
    if request.method == 'POST':
        form = ExpenseEditForm(instance=expense, data=request.POST, owner=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Despesa editada com sucesso.')
            return redirect('core:expenses')
        else:
            return render(request, 'core/expenses_edit.html', {
                'expense': expense,
                'form': form,
            })
    else:
        form = ExpenseEditForm(instance=expense, owner=request.user)
        return render(request, 'core/expenses_edit.html', {
            'expense': expense,
            'form': form,
        })


# FIXME: find a better way to save multiple forms
def expenses_include(request):
    if request.method == 'POST':
        form = ExpenseForm(request.user, request.POST)
        if form.is_valid():
            repeat = form.save(commit=False, user=request.user)
            for expense in range(1, repeat.recurrence):
                print('expense', expense)
                form = ExpenseForm(request.user, request.POST)
                expense = form.save(user=request.user)

            messages.add_message(request, messages.SUCCESS, 'sua despesa foi cadastrada com sucesso'.format(request.user))
            return redirect('core:expenses')
        else:
            return render(request, 'core/expenses_include.html', {
                'form': form,
            })
    else:
        form = ExpenseForm(request.user)
        return render(request, 'core/expenses_include.html', {
            'form': form,
        })


def revenues_include(request):
    if request.method == 'POST':
        form = RevenueForm(request.user, request.POST)
        if form.is_valid():
            revenue = form.save(commit=False)
            revenue.user = request.user
            revenue.save()
            messages.add_message(request, messages.SUCCESS, 'sua receita foi cadastrada com sucesso')
            return redirect('core:index')
        else:
            return render(request, 'core/revenues_include.html', {
                'form': form,
            })
    else:
        form = ExpenseForm(request.user)
        return render(request, 'core/revenues_include.html', {
            'form': form,
        })


# TODO: include revenues edit form
def revenues_edit(request, revenue_id):
    revenue = Revenue.objects.filter(user=request.user).get(id=revenue_id)

    if request.method != 'POST':
        form = RevenueEditForm(instance=revenue, owner=request.user)
    else:
        form = RevenueEditForm(instance=revenue, owner=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'sua receita foi editada com sucesso')
            return redirect('core:index')
        else:
            return render(request, 'core/revenues_edit.html', {
                'form': form,
                'revenue': revenue,
            })
    return render(request, 'core/revenues_edit.html', {
        'form': form,
        'revenue': revenue,
    })


def bank_accounts_create(request):
    if request.method == 'POST':
        form = BankAccountCreateForm(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.owner = request.user
            bank_account.save()
            messages.add_message(request, messages.SUCCESS, 'Parabéns, sua conta foi criada com sucesso!')
            return redirect('core:index')
        else:
            return render(request, 'core/bank_accounts_create.html', {
                'form': form,
            })
    else:
        form = BankAccountCreateForm()
        return render(request, 'core/bank_accounts_create.html', {
            'form': form,
        })


def categories_detail(request, category_slug):
    category = Category.objects.filter(owner=request.user).get(slug=category_slug)
    expenses = category.expenses.filter(user=request.user)
    revenues = category.revenues.filter(user=request.user)
    return render(request, 'core/categories_detail.html', {
        'category': category,
        'expenses': expenses,
        'revenues': revenues,
    })
