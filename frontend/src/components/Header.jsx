import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header className="header">
      <h2>Coffee MiniApp</h2>
      <nav>
        <Link to="/">Главная</Link>
        <Link to="/checkout">Корзина</Link>
      </nav>
    </header>
  );
}