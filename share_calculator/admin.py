from django.contrib import admin
from .models import Account, Holding, Position, Sale

admin.site.register(Account)
admin.site.register(Holding)
admin.site.register(Position)
admin.site.register(Sale)
