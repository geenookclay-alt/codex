import { Nav } from '../../components/nav';

export default function Page() {
  return (
    <section className="space-y-4">
      <Nav />
      <h1 className="text-2xl font-semibold">Upload Queue</h1>
      <p className="text-slate-300">Schedule uploads and monitor pipeline task states.</p>
    </section>
  );
}
