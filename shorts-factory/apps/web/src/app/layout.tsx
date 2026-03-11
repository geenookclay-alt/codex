import './globals.css';
import Link from 'next/link';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100">
        <nav className="border-b border-slate-800 p-4 flex gap-4 text-sm">
          {['dashboard','projects','strategies','queue','analytics','settings','login'].map((r) => (
            <Link key={r} href={`/${r}`} className="hover:text-sky-300 capitalize">{r}</Link>
          ))}
        </nav>
        <main className="p-6">{children}</main>
      </body>
    </html>
  );
}
