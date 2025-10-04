export default function ProductCard({ product, onBuy }) {
    return (
      <div className="product-card">
        <img src={product.image} alt={product.name} width="150" />
        <h4>{product.name}</h4>
        <p>{product.price} ₽</p>
        <button onClick={() => onBuy(product)}>Купить</button>
      </div>
    );
}  