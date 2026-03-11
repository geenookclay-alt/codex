import Link from "next/link";

const pages = ["dashboard", "inbox", "projects", "strategies", "build", "queue", "analytics", "recommendations", "settings", "login"];

export default function Home() {
  return (
    <main className="p-6">
      <h1 className="text-3xl font-semibold">Shorts Factory v8</h1>
      <ul className="mt-4 grid grid-cols-2 gap-3">
        {pages.map((p) => (
          <li key={p} className="rounded border border-slate-700 p-3 hover:bg-slate-900">
            <Link href={`/${p}`}>{p}</Link>
          </li>
        ))}
      </ul>
    </main>
  );
}
