from django.contrib import admin
from .models import Conversion


@admin.register(Conversion)
class ConversionAdmin(admin.ModelAdmin):
    list_display = ("product", "button_label", "timestamp", "referrer")
    list_filter = ("product",)
    ordering = ("-timestamp",)
