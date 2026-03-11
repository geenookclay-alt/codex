import { Nav } from '../../components/nav';

export default function Page() {
  return (
    <section className="space-y-4">
      <Nav />
      <h1 className="text-2xl font-semibold">Analytics</h1>
      <p className="text-slate-300">Performance charts, watch-time trends, and retention breakdowns.</p>
    </section>
  );
}
