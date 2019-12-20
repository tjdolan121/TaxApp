from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib import messages
import datetime
from .models import Account, Holding, Position, Sale
from .forms import SaleForm, HoldingForm


# --------------------------- View functions ---------------------------|


def base_view(request):
    user = request.user
    account = Account.objects.get(user=user)
    holdings = list(Holding.objects.filter(account=account))
    return render(request, template_name='base.html', context={'account': account,
                                                               'holdings': holdings,
                                                               'user': user})


def home_view(request):
    user = request.user
    account = Account.objects.get(user=user)
    holdings = account.holdings.all()
    return render(request, template_name='home.html', context={'user': user,
                                                               'account': account,
                                                               'holdings': holdings})


def holding_view(request, holding):
    user = request.user
    account = Account.objects.get(user=user)
    holding = Holding.objects.get(ticker=holding, account=account)
    holdings = list(Holding.objects.filter(account=account))
    total_shares = get_total_shares(holding)
    return render(request, template_name='holding.html', context={'user': user,
                                                                  'account': account,
                                                                  'holding': holding,
                                                                  'holdings': holdings,
                                                                  'total_shares': total_shares})


def reset_holdings_view(request):
    user = request.user
    if request.method == "POST":
        reset_holdings(user)
        initialize_holdings(user)
        initialize_positions(user)
        return redirect('/')
    return render(request, 'reset_holdings.html')


def create_holding_view(request):
    user = request.user
    account = Account.objects.get(user=user)
    if request.method == 'POST':
        holding_form = HoldingForm(data=request.POST)
        if holding_form.is_valid():
            ticker = holding_form.cleaned_data['ticker']
            if account.holdings.filter(ticker=ticker):
                messages.error(request, "Error, you already own shares in that company")
                return redirect('home')
            else:
                new_holding = holding_form.save(commit=False)
                new_holding.ticker = holding_form.cleaned_data['ticker']
                new_holding.account = account
                new_holding.save()
                return redirect('home')
    else:
        holding_form = HoldingForm()
    return render(request, template_name='new_holding.html', context={'user': user,
                                                                      'account': account,
                                                                      'form': holding_form})


def trade_shares_view(request, holding):
    user = request.user
    account = Account.objects.get(user=user)
    holding = Holding.objects.get(ticker=holding, account=account)
    holdings = list(Holding.objects.filter(account=account))
    next = request.POST.get('next', '/')
    total_shares = get_total_shares(holding)
    if request.method == 'POST':
        sale_form = SaleForm(data=request.POST)
        if sale_form.is_valid():
            new_sale = sale_form.save(commit=False)
            new_sale.user = user
            new_sale.holding = holding
            sale_quantity = sale_form.cleaned_data['sale_quantity']
            sale_price = sale_form.cleaned_data['sale_price']
            # Update attributes
            if sale_form.cleaned_data['type'] == 'Sell':
                if sale_quantity > total_shares or sale_quantity <= 0:
                    messages.error(request, "Error, please enter a valid sale quantity")
                    return redirect('home')
                if sale_price <= 0:
                    messages.error(request, "Error, please enter a valid sale price")
                    return redirect('home')
                sell_shares(account, holding, sale_quantity, sale_price)
                new_sale.cash_after_sale = account.cash
                new_sale.capital_gains_after_sale = account.capital_gains
                new_sale.capital_losses_after_sale = account.capital_losses
                # Save objects
                account.save()
                new_sale.save()
                return HttpResponseRedirect(next)
            else:
                date = sale_form.cleaned_data['date']
                buy_shares(account, holding, sale_quantity, sale_price, date)
                new_sale.cash_after_sale = account.cash
                new_sale.capital_gains_after_sale = account.capital_gains
                new_sale.capital_losses_after_sale = account.capital_losses
                # Save objects
                account.save()
                new_sale.save()
                return HttpResponseRedirect(next)
    else:
        sale_form = SaleForm()

    return render(request, template_name='trade_shares.html', context={'user': user,
                                                                       'account': account,
                                                                       'holding': holding,
                                                                       'form': sale_form,
                                                                       'holdings': holdings,
                                                                       'total_shares': total_shares})


# ------------------------- Helper functions -------------------------|

def get_total_shares(holding):
    positions = holding.positions.all()
    return sum([position.quantity for position in positions])


def get_position(holding):
    current_positions = []
    for position in holding.positions.all():
        if position.quantity > 0:
            current_positions.append(position)
    return current_positions


def buy_shares(account, holding, sale_quantity, sale_price, date):
    new_position = Position(holding=holding, cost_basis=sale_price, quantity=sale_quantity, acquired=date)
    new_position.save()
    cost = sale_price * sale_quantity
    account.cash -= cost
    account.save()


def sell_shares(account, holding, sale_quantity, sale_price):
    initial_sale_quantity = sale_quantity
    positions = holding.positions.all()
    if sale_quantity > get_total_shares(holding):
        return False
    else:
        for position in positions:
            if position.quantity >= sale_quantity:
                position.quantity -= sale_quantity
                return_from_position = sale_quantity * (sale_price - position.cost_basis)
                if return_from_position < 0:
                    account.capital_losses += abs(return_from_position)
                else:
                    account.capital_gains += return_from_position
                position.save()
                break
            elif position.quantity < sale_quantity:
                return_from_position = position.quantity * (sale_price - position.cost_basis)
                sale_quantity -= position.quantity
                if return_from_position < 0:
                    account.capital_losses += abs(return_from_position)
                else:
                    account.capital_gains += return_from_position
                position.quantity = 0
                position.save()
                continue
    account.cash += initial_sale_quantity * sale_price
    return True


def reset_holdings(user):
    account = Account.objects.get(user=user)
    account.cash = 100000.00
    account.capital_gains = 0.00
    account.capital_losses = 0.00
    account.holdings.all().delete()
    account.save()


def initialize_holdings(user):
    account = Account.objects.get(user=user)
    ticker_symbols = set()
    for position in positions:
        ticker_symbols.add(position[4])
    for symbol in ticker_symbols:
        holding = Holding(ticker=symbol, account=account)
        holding.save()
    # holdings = account.holdings.all()


def initialize_positions(user):
    account = Account.objects.get(user=user)
    for position in positions:
        holding = account.holdings.get(ticker=position[4])
        position = Position(holding=holding, acquired=format_date(position[3]), cost_basis=position[2] / 100,
                            quantity=position[1])
        position.save()


def format_date(date):
    d = datetime.datetime.strptime(date, '%m/%d/%Y')
    d.strftime('%Y-%m-%d')
    return d


# ------------------------------ Data -----------------------------|


positions = []
