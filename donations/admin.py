from django.contrib import admin
from .models import Donation


class DonationAdmin(admin.ModelAdmin):
    """
    donation table order
    """

    readonly_fields = ('donation_number', 'record_added',
                       'donation_total',
                       'stripe_pid')

    list_display = ('donation_number', 'production', 'record_added',
                    'donation_total', 'city',
                    'full_name',
                    'stripe_pid')

    ordering = ('-record_added',)


admin.site.register(Donation, DonationAdmin)
