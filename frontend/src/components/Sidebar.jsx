export default function Sidebar({ categories, onFilter }) {
    return (
      <aside className="sidebar">
        <h3>Каталог</h3>
        <ul>
          <li onClick={() => onFilter(null)}>Все</li>
          {categories.map((c) => (
            <li key={c.id} onClick={() => onFilter(c.id)}>
              {c.name}
            </li>
          ))}
        </ul>
      </aside>
    );
  }  