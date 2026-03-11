import { Nav } from '../../components/nav';

export default function Page() {
  return (
    <section className="space-y-4">
      <Nav />
      <h1 className="text-2xl font-semibold">Login</h1>
      <p className="text-slate-300">Authenticate with JWT and continue to workspace.</p>
    </section>
  );
}
