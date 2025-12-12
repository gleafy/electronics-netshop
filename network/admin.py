from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import NetworkNode, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "city",
        "country",
        "supplier_link",
        "level",
        "node_type",
        "debt",
        "created_at",
    )
    list_filter = ("city", "country", "node_type")
    list_select_related = ("supplier",) 
    actions = ["clear_debt"]

    @admin.display(description="Поставщик")
    def supplier_link(self, obj):
        if obj.supplier:
            link = reverse("admin:network_networknode_change", args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', link, obj.supplier.name)
        return "-"

    @admin.action(description="Очистить задолженность перед поставщиком")
    def clear_debt(self, request, queryset):
        count = queryset.update(debt=0.00)
        self.message_user(request, f"Задолженность успешно очищена у {count} объектов.")