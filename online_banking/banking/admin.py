# banking/admin.py
from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance_display')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('user',) # Typically don't change the user association

    def balance_display(self, obj):
        return f"₹{obj.balance:.2f}"
    balance_display.short_description = 'Balance'