def create_invoice_payload(order_id: int) -> str:
    """
    Создаёт payload для Telegram Payments.
    Payload возвращается в successful_payment и используется
    для идентификации заказа.
    """
    return f"order:{order_id}"
