from django.db import models
from users.models import CustomUser
import datetime

SALE_TYPE = (('Buy', 'Buy'), ('Sell', 'Sell'),)


class Account(models.Model):
    cash = models.DecimalField(max_digits=14, decimal_places=2)
    capital_gains = models.DecimalField(max_digits=14, decimal_places=2)
    capital_losses = models.DecimalField(max_digits=14, decimal_places=2)
    net_capital_gains = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"

    def save(self, *args, **kwargs):
        self.net_capital_gains = self.capital_gains - self.capital_losses
        super(Account, self).save(*args, **kwargs)


class Holding(models.Model):
    ticker = models.CharField(max_length=10)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='holdings')

    def __str__(self):
        return f"{self.account}: {self.ticker}"


class Position(models.Model):
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, related_name='positions')
    acquired = models.DateTimeField()
    cost_basis = models.DecimalField(max_digits=14, decimal_places=2)
    is_shortterm = models.BooleanField(default=False)
    quantity = models.DecimalField(max_digits=14, decimal_places=2)

    def __str__(self):
        return f"{self.holding.account.user} | {self.acquired} | \
        {self.holding.ticker} @ {self.cost_basis}: {self.quantity} shares"

    def check_if_shortterm(self):
        current_year = datetime.date.today().year
        if self.acquired.year == current_year:
            return True
        else:
            return False

    def save(self, *args, **kwargs):
        current_year = datetime.date.today().year
        if self.acquired.year == current_year:
            self.is_shortterm = True
        else:
            self.is_shortterm = False
        super(Position, self).save(*args, **kwargs)

    class Meta:
        ordering = ['acquired']


class Sale(models.Model):
    type = models.CharField(max_length=7, choices=SALE_TYPE, default='Sell')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sales', default=1)
    holding = models.ForeignKey(Holding, on_delete=models.CASCADE, related_name='sales')
    date = models.DateTimeField()
    sale_quantity = models.DecimalField(max_digits=14, decimal_places=2)
    sale_price = models.DecimalField(max_digits=14, decimal_places=2)
    cash_after_sale = models.DecimalField(max_digits=14, decimal_places=2)
    capital_gains_after_sale = models.DecimalField(max_digits=14, decimal_places=2)
    capital_losses_after_sale = models.DecimalField(max_digits=14, decimal_places=2)
    net_capital_gains_after_sale = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    target = models.DecimalField(max_digits=14, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.holding.account.user} | {self.date} | {self.sale_quantity} @ ${self.sale_price}"

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        self.net_capital_gains_after_sale = self.capital_gains_after_sale - self.capital_losses_after_sale
        super(Sale, self).save(*args, **kwargs)
