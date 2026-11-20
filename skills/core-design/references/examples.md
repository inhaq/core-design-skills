# Before and after

Read this file when you need a concrete fix for a common tell, or when a review needs a worked example. Each pair shows the AI-default first, then the fix. Tailwind is used for brevity; the same fix applies in any CSS method. "After" code uses token classes (`bg-surface-2`, `text-fg`, `bg-warning-subtle`) mapped to your theme, not Tailwind's default palette.

## Contents

1. [Active nav item](#1-active-nav-item)
2. [Callout](#2-callout)
3. [Hero headline](#3-hero-headline)
4. [Hero CTAs](#4-hero-ctas)
5. [Feature grid](#5-feature-grid)
6. [Nested card](#6-nested-card)
7. [Stats row](#7-stats-row)
8. [Empty state](#8-empty-state)
9. [Form field error](#9-form-field-error)
10. [Scroll reveal](#10-scroll-reveal)

## 1. Active nav item

```html
<!-- Before: left bar is the only active signal -->
<a class="border-l-4 border-indigo-500 pl-3 text-indigo-600">Projects</a>

<!-- After: tint + weight, plus aria-current -->
<a aria-current="page" class="rounded-md bg-surface-2 px-3 font-medium text-fg">Projects</a>
```

## 2. Callout

```html
<!-- Before: docs-template stripe -->
<div class="border-l-4 border-amber-500 bg-amber-50 p-4">Back up first.</div>

<!-- After: tint, icon, bold lead word; no stripe -->
<div role="note" class="flex gap-3 rounded-lg bg-warning-subtle p-4 text-warning-fg">
  <svg aria-hidden="true" class="mt-0.5 size-4 shrink-0">…</svg>
  <p><strong>Back up first.</strong> The migration rewrites every row.</p>
</div>
```

## 3. Hero headline

```html
<!-- Before: eyebrow + staccato + one italic word -->
<p class="uppercase tracking-widest text-sm">Introducing</p>
<h1>Ship <em class="font-serif">faster</em>. Build better.</h1>

<!-- After: one specific claim -->
<h1 class="text-balance">Deploy previews for every pull request, in under a minute.</h1>
```

## 4. Hero CTAs

```html
<!-- Before: two equal buttons -->
<button class="btn-primary">Get started free</button>
<button class="btn-primary">Learn more</button>

<!-- After: one primary, one quiet link -->
<button class="btn-primary">Start a free project</button>
<a href="/docs" class="underline underline-offset-4">Read the docs</a>
```

## 5. Feature grid

```html
<!-- Before: six identical cards, icon in a colored circle -->
<div class="grid grid-cols-3 gap-6">
  <div class="card"><span class="rounded-full bg-indigo-100 p-3">…</span><h3>Fast</h3><p>…</p></div>
  <!-- ×6 -->
</div>

<!-- After: one lead feature, the rest as a plain list -->
<section class="grid gap-12 md:grid-cols-[2fr_1fr]">
  <article><h3>Branch previews</h3><p>…</p><img src="/previews.png" alt="Preview link on a pull request" width="960" height="600" /></article>
  <ul class="space-y-4"><li><strong>Rollbacks</strong> in one click.</li>…</ul>
</section>
```

## 6. Nested card

```css
/* Before: same radius, border + ring + shadow on both */
.panel, .panel > .card { border-radius: 16px; border: 1px solid #e5e5e5; box-shadow: 0 4px 12px rgb(0 0 0 / .1); }

/* After: concentric radius, one edge treatment, inner surface by tone */
.panel { --radius: 16px; --pad: 8px; border-radius: var(--radius); padding: var(--pad); box-shadow: var(--shadow-sm); }
.panel > .card { border-radius: calc(var(--radius) - var(--pad)); background: var(--surface-2); }
```

## 7. Stats row

```html
<!-- Before: invented numbers -->
<div>10k+ users</div><div>99.9% uptime</div><div>24/7 support</div>

<!-- After: one real number with its source, or cut the row -->
<p><span class="tabular-nums font-medium">1,284</span> teams deployed this week.</p>
```

## 8. Empty state

```html
<!-- Before -->
<p>No data</p>

<!-- After: what goes here, and the action that fills it -->
<div>
  <h3>No invoices yet</h3>
  <p>Invoices appear here after your first paid month.</p>
  <a href="/billing">Add a payment method</a>
</div>
```

## 9. Form field error

```html
<!-- Before: red border only -->
<input class="border-red-500" placeholder="Email" />

<!-- After: label, message, and programmatic link -->
<label for="email">Email</label>
<input id="email" aria-invalid="true" aria-describedby="email-err" class="border-danger" />
<p id="email-err" class="text-danger-fg">Add an @ and a domain, like name@company.com.</p>
```

## 10. Scroll reveal

```css
/* Before: everything hidden until JS adds .visible */
.reveal { opacity: 0; transform: translateY(24px); }
.reveal.visible { opacity: 1; transform: none; transition: all .6s; }

/* After: hidden only when JS is present, exact properties, reduced-motion safe */
.js .reveal { opacity: 0; transform: translateY(12px); }
.js .reveal.visible { opacity: 1; transform: none; transition: opacity 300ms var(--ease-out), transform 300ms var(--ease-out); }
@media (prefers-reduced-motion: reduce) { .js .reveal { transform: none; } }
```

Use reveals for one or two key moments per page, not every block.
