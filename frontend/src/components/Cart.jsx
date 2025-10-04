import { useContext } from "react";
import { CartContext } from "../context/CartContext";

export default function Cart() {
  const { cart, removeFromCart, total } = useContext(CartContext);

  return (
    <div>
      <h2>Корзина</h2>
      {cart.map((item, i) => (
        <div key={i}>
          <b>{item.product.name}</b> ({item.options.milk || "—"}) x {item.quantity}
          = {item.product.price * item.quantity} ₽
          <button onClick={() => removeFromCart(i)}>Удалить</button>
        </div>
      ))}
      <h3>Итого: {total} ₽</h3>
    </div>
  );
}