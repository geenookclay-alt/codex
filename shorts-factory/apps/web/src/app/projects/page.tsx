export default function ProjectsPage() {
  const cards = ['strategy review', 'video preview', 'upload scheduling', 'performance charts'];
  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold capitalize">projects</h1>
      <p className="text-slate-300">Project creation and content asset registration workspace.</p>
      <div className="grid md:grid-cols-2 gap-3">
        {cards.map((item) => (
          <article key={item} className="rounded border border-slate-800 p-4">{item}</article>
        ))}
      </div>
    </section>
  );
}
