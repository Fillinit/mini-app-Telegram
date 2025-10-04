import { useContext } from "react";
import { CartContext } from "../context/CartContext";
import Cart from "../components/Cart";
import { createOrder, sendInvoice } from "../api/api";

export default function Checkout() {
  const { cart, total, clearCart } = useContext(CartContext);

  const handlePay = async () => {
    const order = { items: cart, total };
    const data = await createOrder(order);
    await sendInvoice(data.id); // через Telegram
    clearCart();
    alert("Заказ отправлен! Подтверждение придет в Telegram.");
  };

  return (
    <div>
      <Cart />
      <button onClick={handlePay} disabled={!cart.length}>
        Оплатить
      </button>
    </div>
  );
}