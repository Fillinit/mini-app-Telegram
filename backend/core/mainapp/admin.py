from django.contrib import admin
from django.utils.html import format_html
from .models import Product, ProductOption, Order, OrderItem


class ProductOptionInline(admin.TabularInline):
    """
    Inline для отображения опций товара на странице товара
    """
    model = ProductOption
    extra = 1
    fields = ('name', 'values')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Админ-панель для товаров
    """
    list_display = ('title', 'display_price', 'display_image', 'display_created_at')
    list_filter = ('created_at',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'display_image_preview')
    inlines = (ProductOptionInline,)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'price', 'image')
        }),
        ('Дополнительная информация', {
            'fields': ('meta', 'created_at', 'display_image_preview'),
            'classes': ('collapse',)
        }),
    )

    def display_price(self, obj):
        return f"{obj.price} ₽"
    display_price.short_description = 'Цена'

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "—"
    display_image.short_description = 'Изображение'

    def display_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" style="object-fit: cover;" />', obj.image.url)
        return "Изображение не загружено"
    display_image_preview.short_description = 'Предпросмотр изображения'

    def display_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    display_created_at.short_description = 'Дата создания'


class OrderItemInline(admin.TabularInline):
    """
    Inline для отображения позиций заказа на странице заказа
    """
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price', 'display_options')
    fields = ('product', 'quantity', 'price', 'display_options')
    can_delete = False

    def display_options(self, obj):
        if obj.options:
            options_text = []
            for key, value in obj.options.items():
                options_text.append(f"{key}: {value}")
            return ", ".join(options_text)
        return "—"
    display_options.short_description = 'Опции'

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Админ-панель для заказов
    """
    list_display = ('id', 'telegram_user_id', 'status', 'display_total', 'created_at', 'address')
    list_filter = ('status', 'created_at')
    search_fields = ('id', 'telegram_user_id', 'address')
    readonly_fields = ('created_at', 'display_items', 'display_created_at')
    inlines = (OrderItemInline,)
    fieldsets = (
        ('Основная информация', {
            'fields': ('telegram_user_id', 'status', 'total', 'address')
        }),
        ('Дополнительная информация', {
            'fields': ('extra', 'display_created_at', 'display_items'),
            'classes': ('collapse',)
        }),
    )
    actions = ['mark_as_paid', 'mark_as_completed', 'mark_as_rejected']

    def display_total(self, obj):
        return f"{obj.total} ₽"
    display_total.short_description = 'Сумма'

    def display_items(self, obj):
        items = obj.items.all()
        if items:
            items_text = []
            for item in items:
                items_text.append(f"{item.product.title} x{item.quantity} - {item.price}₽")
            return format_html("<br>".join(items_text))
        return "—"
    display_items.short_description = 'Состав заказа'

    def display_created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M:%S')
    display_created_at.short_description = 'Дата создания'

    def created_at(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')
    created_at.short_description = 'Дата создания'

    @admin.action(description="Отметить как оплаченные")
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status=Order.StatusType.PAID)
        self.message_user(request, f"{updated} заказов отмечены как оплаченные")

    @admin.action(description="Отметить как завершенные")
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status=Order.StatusType.COMPLETED)
        self.message_user(request, f"{updated} заказов отмечены как завершенные")

    @admin.action(description="Отметить как отклоненные")
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status=Order.StatusType.REJECTED)
        self.message_user(request, f"{updated} заказов отмечены как отклоненные")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Админ-панель для позиций заказа
    """
    list_display = ('id', 'order', 'product', 'quantity', 'display_price', 'display_options')
    list_filter = ('order__status',)
    search_fields = ('order__id', 'product__title')
    readonly_fields = ('order', 'product', 'quantity', 'price', 'options')

    def display_price(self, obj):
        return f"{obj.price} ₽"
    display_price.short_description = 'Цена'

    def display_options(self, obj):
        if obj.options:
            options_text = []
            for key, value in obj.options.items():
                options_text.append(f"{key}: {value}")
            return ", ".join(options_text)
        return "—"
    display_options.short_description = 'Опции'


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    """
    Админ-панель для опций товаров
    """
    list_display = ('product', 'name', 'display_values')
    list_filter = ('product',)
    search_fields = ('product__title', 'name')

    def display_values(self, obj):
        if obj.values:
            return ", ".join(str(v) for v in obj.values)
        return "—"
    display_values.short_description = 'Значения'