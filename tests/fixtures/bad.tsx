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
