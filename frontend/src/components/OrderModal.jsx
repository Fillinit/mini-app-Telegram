import { useState } from "react";

export default function OrderModal({ product, onClose, onConfirm }) {
  const [milk, setMilk] = useState("обычное");
  const [quantity, setQuantity] = useState(1);

  if (!product) return null;

  return (
    <div className="modal">
      <h3>{product.name}</h3>
      {product.category === "coffee" && (
        <div>
          <label>Молоко:</label>
          <select value={milk} onChange={(e) => setMilk(e.target.value)}>
            <option value="обычное">Обычное</option>
            <option value="соевое">Соевое</option>
            <option value="овсяное">Овсяное</option>
          </select>
        </div>
      )}
      <div>
        <label>Количество:</label>
        <input
          type="number"
          value={quantity}
          min="1"
          onChange={(e) => setQuantity(parseInt(e.target.value))}
        />
      </div>
      <button onClick={() => onConfirm(product, { milk }, quantity)}>Добавить</button>
      <button onClick={onClose}>Отмена</button>
    </div>
  );
}