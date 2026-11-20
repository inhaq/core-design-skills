// Each line carries the tell named in the trailing comment. Line numbers are asserted in tests.
<a className="border-s-4 border-accent">Projects</a> {/* left-edge accent bar */}
<a style={{ borderInlineStart: 0 }} className="shadow-[inset_3px_0_0_var(--accent)]">Inbox</a> {/* left-edge bar via inset shadow */}
<a className="relative before:absolute before:left-0 before:w-1 before:bg-accent">Team</a> {/* left-edge bar via ::before */}
<p className="tracking-widest uppercase">Features</p> {/* wide uppercase tracking */}
<section className="h-screen">Hero</section> {/* h-screen */}
<button className="transition-all">Go</button> {/* transition: all */}
<button className="focus:outline-none">Go</button> {/* focus outline removed */}
<div
  className="row"
  onClick={open}>Row</div> {/* div with onClick, starts on line 9 */}
<h1>Unleash your workflow</h1> {/* buzzword copy */}
<a className="border-l-4">Kept</a> {/* check-tells: ignore — design review approved */}
// The ignore pragma above covers the next line too, so this line stays a comment.
<button className="focus-visible:outline-none">Save</button> {/* focus outline removed: focus-visible */}
<input className="focus:outline-none focus:ring-0" /> {/* focus outline removed: ring-0 removes the ring too */}
<input className="focus:outline-hidden" /> {/* focus outline removed: Tailwind v4 */}
<div onKeyDown={(e) => e.key === "Enter" && open()} onClick={open}>Row</div> {/* div with onClick after an arrow function */}
<h1>Ship <em>faster</em> today</h1> {/* italic or gradient word in headline */}
