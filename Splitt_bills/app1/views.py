from django.shortcuts import render, redirect
from .models import User, Expense, Balance

def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'users': users})


def add_expense(request):
    users = User.objects.all()

    if request.method == 'POST':
        payer_name = request.POST.get('payer')
        participants_names = request.POST.getlist('participants')
        amount = float(request.POST.get('amount'))
        expense_type = request.POST.get('expense_type')
        payer = User.objects.get(name=payer_name)
        participants = User.objects.filter(name__in=participants_names).exclude(name=payer_name)
        expense = Expense.objects.create(
            payer=payer,
            amount=amount,
            expense_type=expense_type
        )
        expense.participants.add(*participants)
        expense.save()

        if expense.expense_type == 'EQUAL':
            update_equal_expense_balances(expense)
        elif expense.expense_type == 'EXACT':
            exact_amounts = [float(value) for value in request.POST.getlist('exact_amounts')]
            if sum(exact_amounts) > amount:
                return render(request, 'add_expense.html', {'users': users, 'error': 'The sum of exact amounts must equal the total amount.'})
            update_exact_expense_balances(expense, exact_amounts)
        elif expense.expense_type == 'PERCENT':
            percent_amounts = [float(value) for value in request.POST.getlist('percent_amounts')]
            if sum(percent_amounts) > 100:
                return render(request, 'add_expense.html', {'users': users, 'error': 'The sum of percentages must equal 100.'})
            update_percent_expense_balances(expense, percent_amounts)

        return redirect('index')

    return render(request, 'add_expense.html', {'users': users})

def update_equal_expense_balances(expense):
    amount_per_person = expense.amount / (expense.participants.count() + 1)

    for participant in expense.participants.all():
        if participant != expense.payer:
            balance, created = Balance.objects.get_or_create(
                creditor=expense.payer,
                debtor=participant,
                defaults={'amount': amount_per_person}
            )
            if not created:
                balance.amount = float(balance.amount) +  amount_per_person
                balance.save()

def update_exact_expense_balances(expense, post_data):
    for i,participant in enumerate(expense.participants.all()):
        if participant != expense.payer:
            amount = post_data[i]
            balance, created = Balance.objects.get_or_create(
                creditor=expense.payer,
                debtor=participant,
                defaults={'amount': amount}
            )
            if not created:
                balance.amount = float(balance.amount) +  amount
                balance.save()

def update_percent_expense_balances(expense, post_data):
    for i, participant in enumerate(expense.participants.all()):
        if participant != expense.payer:
            percentage = post_data[i] / 100
            amount = expense.amount * percentage
            balance, created = Balance.objects.get_or_create(
                creditor=expense.payer,
                debtor=participant,
                defaults={'amount': amount}
            )
            if not created:
                balance.amount = float(balance.amount) +  amount
                balance.save()


def balances(request):
    users = User.objects.all()
    balances = Balance.objects.all()
    return render(request, 'balances.html', {'users': users, 'balances': balances})