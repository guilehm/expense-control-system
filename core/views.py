import logging

from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms.models import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from bank.models import BankAccount
from core.forms import BankAccountCreateForm, CategoryIncludeForm, CSVImportForm
from core.models import Category, Tag
from core.tasks import create_tag
from utils.category_importer import process_csv_category_file
from transactions.forms import ExpenseEditForm, ExpenseForm, MultipleExpenseEditForm, RevenueEditForm, RevenueForm
from transactions.models import Expense, Revenue

# Create your views here.
logger = logging.getLogger('controller')


def index(request):
    if request.user.is_authenticated:
        accounts = BankAccount.objects.prefetch_related(
            'bank',
        ).filter(owner=request.user)
        expenses = Expense.objects.prefetch_related(
            'account',
            'category',
            'tags',
        ).filter(user=request.user).order_by('due_date')
        revenues = Revenue.objects.prefetch_related(
            'account',
            'category',
            'tags',
        ).filter(user=request.user).order_by('due_date')
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
            messages.add_message(
                request,
                messages.SUCCESS,
                'Olá, {}, seu login foi efetuado com sucesso'.format(request.user)
            )
            return redirect('core:index')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'login_form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:index'))


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('core:index')
        else:
            if form.errors:
                return render(request, 'core/register.html', context)
    else:
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'core/register.html', context)


def expense_list(request):
    expenses = Expense.objects.prefetch_related(
        'account',
        'category',
    ).filter(
        user=request.user
    )
    categories = Category.objects.filter(owner=request.user)
    tags = Tag.objects.filter(owner=request.user)

    expense_edit_form = modelformset_factory(Expense, form=MultipleExpenseEditForm, extra=0)
    formset = expense_edit_form(request.POST or None, queryset=expenses)
    for form in formset.forms:
        form.fields['account'].queryset = BankAccount.objects.filter(owner=request.user)
        form.fields['category'].queryset = Category.objects.filter(owner=request.user)

    if formset.is_valid():
        instances = formset.save(commit=False)
        count = 0
        for instance in instances:
            count += 1
            instance.save()
    else:
        count = 0

    return render(request, 'core/expenses.html', {
        'expenses': expenses,
        'categories': categories,
        'tags': tags,
        'formset': formset,
        'count': count,
    })


def revenue_list(request):
    categories = Category.objects.filter(owner=request.user)
    revenues = Revenue.objects.prefetch_related(
        'category',
    ).filter(user=request.user)
    tags = Tag.objects.filter(owner=request.user)
    return render(request, 'core/revenues.html', {
        'revenues': revenues,
        'categories': categories,
        'tags': tags,
    })


def expense_edit(request, expense_id):
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
        form = ExpenseEditForm(instance=expense, owner=request.user)
        return render(request, 'core/expenses_edit.html', {
            'expense': expense,
            'form': form,
        })


# FIXME: find a better way to save multiple forms
def expense_include(request):
    if request.method != 'POST':
        form = ExpenseForm(request.user)
    else:
        form = ExpenseForm(request.user, request.POST)
        if form.is_valid():
            expense = form.save(user=request.user)
            due_date = expense.due_date
            delta = due_date + relativedelta(months=1)
            for loop in range(1, expense.recurrence):
                Expense.objects.create(
                    user=request.user,
                    account=expense.account,
                    title=expense.title,
                    description=expense.description,
                    total=expense.total,
                    competition_date=expense.competition_date,
                    due_date=delta,
                    paid_out=expense.paid_out,
                    note=expense.note,
                )
                delta = delta + relativedelta(months=1)

            messages.add_message(
                request,
                messages.SUCCESS,
                'sua despesa foi cadastrada com sucesso'.format(request.user)
            )
            return redirect('core:expenses')
    return render(request, 'core/expenses_include.html', {
        'form': form,
    })


def revenue_include(request):
    if request.method == 'POST':
        form = RevenueForm(request.user, request.POST)
        if form.is_valid():
            revenue = form.save(commit=False)
            revenue.user = request.user
            revenue.save()
            messages.add_message(request, messages.SUCCESS, 'sua receita foi cadastrada com sucesso')
            return redirect('core:revenues')
    else:
        form = ExpenseForm(request.user)
        return render(request, 'core/revenues_include.html', {
            'form': form,
        })


# TODO: include revenues edit form
def revenue_edit(request, revenue_id):
    revenue = Revenue.objects.filter(user=request.user).get(id=revenue_id)

    if request.method != 'POST':
        form = RevenueEditForm(instance=revenue, owner=request.user)
    else:
        form = RevenueEditForm(instance=revenue, owner=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'sua receita foi editada com sucesso')
            return redirect('core:revenues')

    return render(request, 'core/revenues_edit.html', {
        'form': form,
        'revenue': revenue,
    })


def bank_account_create(request):
    form = BankAccountCreateForm()
    if request.method == 'POST':
        form = BankAccountCreateForm(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.owner = request.user
            bank_account.save()
            messages.add_message(request, messages.SUCCESS, 'Parabéns, sua conta foi criada com sucesso!')
            return redirect('core:index')
    return render(request, 'core/bank_accounts_create.html', {
        'form': form,
    })


def category_detail(request, category_slug):
    category = Category.objects.filter(owner=request.user).get(slug=category_slug)
    expenses = category.expenses.filter(user=request.user)
    revenues = category.revenues.filter(user=request.user)
    return render(request, 'core/categories_detail.html', {
        'category': category,
        'expenses': expenses,
        'revenues': revenues,
    })


def category_include(request):
    if request.method != 'POST':
        form = CategoryIncludeForm()
    else:
        form = CategoryIncludeForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = request.user
            category.save()
            messages.add_message(request, messages.SUCCESS, 'Parabéns, sua categoria foi criada com sucesso!')
            return redirect('core:categories-include')
        return render(request, 'core/categories_include.html', {
            'form': form,
        })

    return render(request, 'core/categories_include.html', {
        'form': form,
    })


def category_import(request):
    if request.method != 'POST':
        form = CSVImportForm()
    else:
        form = CSVImportForm(request.POST, request.FILES)
        if form.is_valid():
            csv = form.save(commit=False)
            csv.owner = request.user
            csv.save()
            messages.add_message(request, messages.SUCCESS, 'Arquivo salvo com sucesso!')
            process_csv_category_file(csv)  #TODO: make this an async task
    return render(request, 'core/categories_import.html', {
        'form': form,
    })


def api_list(request):
    return render(request, 'core/api_list.html')


def test_celery(request):
    create_tag.delay()
