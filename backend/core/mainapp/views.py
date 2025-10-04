from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import requests
import json
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


# Константы для Telegram API
TELEGRAM_API_URL = "https://api.telegram.org/bot"
TELEGRAM_BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
PAYMENT_PROVIDER_TOKEN = settings.PAYMENT_PROVIDER_TOKEN


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet для работы с товарами (только чтение)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления заказами
    
    Предоставляет стандартные CRUD операции для заказов,
    а также дополнительные действия для работы с платежами и статусами.
    """
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def _send_telegram_message(self, chat_id, text):
        """
        Вспомогательный метод для отправки сообщений в Telegram
        """
        url = f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {'chat_id': chat_id, 'text': text}
        try:
            response = requests.post(url, data=payload)
            return response
        except requests.RequestException:
            # Логирование ошибки можно добавить здесь
            return None

    @action(detail=True, methods=['POST'])
    def send_invoice(self, request, pk=None):
        """
        POST /api/orders/{id}/send_invoice/

        **Описание:**
        Отправляет счет на оплату заказа через Telegram Bot API.
        Создает инвойс с деталями заказа для оплаты пользователем.

        **Параметры:**
        - id: ID заказа (в URL)

        **Требуемые настройки:**
        - TELEGRAM_BOT_TOKEN: BOT_TOKEN
        - PAYMENT_PROVIDER_TOKEN: токен платежного провайдера

        **Возвращает:**
        - ok: статус выполнения запроса
        - resp: ответ от Telegram API или текст ошибки
        """
        order = self.get_object()
        chat_id = order.telegram_user_id

        # Формируем данные для инвойса
        prices = [{
            "label": f"Заказ #{order.id}",
            "amount": int(order.total * 100)  # Сумма в копейках
        }]
        
        payload = {
            'chat_id': chat_id,
            'title': f'Оплата заказа #{order.id}',
            'description': f'Оплата заказа на сумму {order.total} руб.',
            'payload': str(order.id),
            'provider_token': PAYMENT_PROVIDER_TOKEN,
            'start_parameter': f'order_{order.id}',
            'currency': 'RUB',
            'prices': json.dumps(prices)
        }
        
        # Отправляем инвойс через Telegram API
        url = f"{TELEGRAM_API_URL}{TELEGRAM_BOT_TOKEN}/sendInvoice"
        response = requests.post(url, data=payload)
        
        return Response({
            'ok': response.ok, 
            'resp': response.json() if response.ok else response.text
        })

    @action(detail=True, methods=['POST'])
    def mark_paid(self, request, pk=None):
        """
        POST /api/orders/{id}/mark_paid/

        **Описание:**
        Помечает заказ как оплаченный и уведомляет пользователя через Telegram.
        Изменяет статус заказа на 'paid' и отправляет подтверждение.

        **Параметры:**
        - id: ID заказа (в URL)

        **Возвращает:**
        - status: результат операции ('ok' при успехе)
        """
        order = self.get_object()
        order.status = 'paid'
        order.save()
        
        # Отправляем уведомление пользователю
        message_text = f'Ваш заказ #{order.id} оплачен. Ожидайте подтверждения.'
        self._send_telegram_message(order.telegram_user_id, message_text)
        
        return Response({'status': 'ok'})

    @action(detail=True, methods=['POST'])
    def set_status(self, request, pk=None):
        """
        POST /api/orders/{id}/set_status/

        **Описание:**
        Изменяет статус заказа на указанный и уведомляет пользователя через Telegram.
        Поддерживает все статусы из STATUS_CHOICES модели Order.

        **Обязательные поля в теле запроса:**
        - status: новый статус заказа (created/paid/accepted/rejected/completed)

        **Параметры:**
        - id: ID заказа (в URL)

        **Возвращает:**
        - status: результат операции ('ok' при успехе)
        """
        order = self.get_object()
        new_status = request.data.get('status')
        
        if not new_status:
            return Response(
                {'error': 'Статус не указан'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = new_status
        order.save()
        
        # Отправляем уведомление пользователю
        message_text = f'Статус вашего заказа #{order.id}: {order.get_status_display()}'
        self._send_telegram_message(order.telegram_user_id, message_text)
        
        return Response({'status': 'ok'})