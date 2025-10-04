from django.db import models


class Product(models.Model):
    """
    Модель товара/продукта
    """
    title = models.CharField(verbose_name="Название товара", max_length=255)
    description = models.TextField(verbose_name="Описание товара", blank=True)
    price = models.DecimalField(
        verbose_name="Цена товара", 
        max_digits=10, 
        decimal_places=2
    )
    image = models.ImageField(upload_to='Продукты/', verbose_name="Изображение", null=True, blank=True)
    meta = models.JSONField(verbose_name="Мета-данные товара", default=dict, blank=True)
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title


class ProductOption(models.Model):
    """
    Модель опций товара (характеристики, варианты выбора)
    """
    product = models.ForeignKey(
        Product, 
        verbose_name="Товар",
        related_name='options', 
        on_delete=models.CASCADE
    )
    name = models.CharField(verbose_name="Название опции", max_length=100)  # например: 'молоко'
    values = models.JSONField(verbose_name="Значения опции", default=list)  # например: ['Цельное','Овсяное','Миндальное']

    class Meta:
        verbose_name = "опцию товара"
        verbose_name_plural = "Опции товаров"

    def __str__(self):
        return f"{self.product.title} - {self.name}"


class Order(models.Model):
    """
    Модель заказа
    """
    class StatusType(models.TextChoices):
        CREATED = "created", "Создан"
        PAID = "paid", "Оплачен"
        ACCEPTED = "accepted", "Принят"
        REJECTED = "rejected", "Отклонен"
        COMPLETED = "completed", "Завершен"
    
    telegram_user_id = models.BigIntegerField(verbose_name="ID пользователя Telegram")
    status = models.CharField(
        verbose_name="Статус заказа", 
        max_length=20, 
        choices=StatusType.choices, 
        default=StatusType.CREATED
    )
    total = models.DecimalField(
        verbose_name="Общая сумма заказа", 
        max_digits=10, 
        decimal_places=2, 
        default=0
    )
    address = models.CharField(verbose_name="Адрес доставки", max_length=512, blank=True)
    extra = models.JSONField(verbose_name="Дополнительная информация", default=dict, blank=True)
    created_at = models.DateTimeField(verbose_name="Дата создания заказа", auto_now_add=True)

    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} - {self.get_status_display()}"


class OrderItem(models.Model):
    """
    Модель позиции в заказе
    """
    order = models.ForeignKey(
        Order, 
        verbose_name="Заказ",
        related_name='items', 
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, 
        verbose_name="Товар",
        on_delete=models.PROTECT
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество", default=1)
    price = models.DecimalField(
        verbose_name="Цена позиции", 
        max_digits=10, 
        decimal_places=2
    )
    options = models.JSONField(
        verbose_name="Выбранные опции", 
        default=dict, 
        blank=True
    )  # например: {'milk': 'oat'}

    class Meta:
        verbose_name = "позицию заказа"
        verbose_name_plural = "Позиции заказов"

    def __str__(self):
        return f"{self.product.title} x{self.quantity} в заказе #{self.order.id}"