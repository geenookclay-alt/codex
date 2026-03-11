const items = ['dashboard','projects','strategies','queue','analytics','settings','login'];

export function Nav() {
  return (
    <nav className="mb-6 flex gap-3 text-sm">
      {items.map((item) => (
        <a key={item} href={`/${item}`} className="rounded bg-slate-800 px-3 py-1 capitalize hover:bg-slate-700">
          {item}
        </a>
      ))}
    </nav>
  );
}
