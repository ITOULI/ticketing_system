from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Ticket,
    TicketImage,
    TicketSpecification,
    TicketSpecificationValue,
    TicketType,
)

admin.site.register(Category, MPTTModelAdmin)


class TicketSpecificationInline(admin.TabularInline):
    model = TicketSpecification


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    inlines = [
        TicketSpecificationInline,
    ]


class TicketImageInline(admin.TabularInline):
    model = TicketImage


class TicketSpecificationValueInline(admin.TabularInline):
    model = TicketSpecificationValue


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = [
        TicketSpecificationValueInline,
        TicketImageInline,
    ]
