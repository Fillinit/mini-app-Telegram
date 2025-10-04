import { useEffect, useState, useContext } from "react";
import { getProducts } from "../api/api";
import { CartContext } from "../context/CartContext";
import Sidebar from "../components/Sidebar";
import ProductCard from "../components/ProductCard";
import OrderModal from "../components/OrderModal";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selected, setSelected] = useState(null);
  const { addToCart } = useContext(CartContext);

  useEffect(() => {
    getProducts().then((data) => {
      setProducts(data);
      setFiltered(data);
      setCategories([...new Set(data.map((p) => ({ id: p.category, name: p.category })))]); 
    });
  }, []);

  const filterByCategory = (catId) => {
    if (!catId) setFiltered(products);
    else setFiltered(products.filter((p) => p.category === catId));
  };

  return (
    <div className="home">
      <Sidebar categories={categories} onFilter={filterByCategory} />
      <div className="products">
        {filtered.map((p) => (
          <ProductCard key={p.id} product={p} onBuy={setSelected} />
        ))}
      </div>
      <OrderModal
        product={selected}
        onClose={() => setSelected(null)}
        onConfirm={(product, options, quantity) => {
          addToCart(product, options, quantity);
          setSelected(null);
        }}
      />
    </div>
  );
}