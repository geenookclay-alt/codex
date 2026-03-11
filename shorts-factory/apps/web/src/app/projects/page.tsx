import { Nav } from '../../components/nav';

export default function Page() {
  return (
    <section className="space-y-4">
      <Nav />
      <h1 className="text-2xl font-semibold">Projects</h1>
      <p className="text-slate-300">Create and manage short-video projects and linked assets.</p>
    </section>
  );
}
