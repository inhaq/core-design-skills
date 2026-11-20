# Anti-patterns to avoid

Read this file when reviewing UI for "AI-default" tells, when a generated design feels generic, or before shipping.

## Contents

- [How to read this file](#how-to-read-this-file)
- [Color and mood](#color-and-mood)
- [Typography](#typography)
- [Layout](#layout)
- [Borders, boxes, and containers](#borders-boxes-and-containers)
- [Components](#components)
- [Icons](#icons)
- [Marketing sections](#marketing-sections)
- [Decoration](#decoration)
- [Motion](#motion)
- [Hierarchy](#hierarchy)
- [Spacing and rhythm](#spacing-and-rhythm)
- [Product UI and dashboards](#product-ui-and-dashboards)
- [Forms](#forms)
- [Content and copy](#content-and-copy)
- [Internationalization](#internationalization)
- [Accessibility and code](#accessibility-and-code)
- [Short rule of thumb](#short-rule-of-thumb)

## How to read this file

Each item is written as **Pattern.** `[tag]` Why it fails, when not obvious. → What to do instead.

Each item carries a tag:

- `[always]` — wrong in every context. Fix it.
- `[default]` — wrong when used by default. Allowed only when the aesthetic direction calls for it and you can say why.

Many of these can be found mechanically. Run `scripts/check-tells.py` (path relative to the skill directory) over the output, then judge each hit by hand. See `references/grep-tells.md`.

## Color and mood

- **Purple, indigo, or blue-to-purple gradients as the brand look.** `[default]` The single most common AI tell. → Pick an accent from the brand or the aesthetic direction; use flat color.
- **Gradient text in headings.** `[default]` Lowers contrast and reads as template. → Solid text; get emphasis from weight or size.
- **Gradient buttons.** `[default]` Startup-template look; hurts the label's contrast. → Flat accent fill with a clear hover state.
- **Neon glow, blurred blobs, glowing orbs.** `[default]` Decoration with no meaning. → Remove, or replace with one deliberate atmosphere choice.
- **Pure black backgrounds with electric accents.** `[default]` Harsh, and every dev-tool template does it. → `#0A0A0A`–`#111` with a muted accent.
- **Colored glow shadow under the primary button** (`shadow-indigo-500/50`). `[default]` Fake energy. → Neutral, low-opacity shadow or none.
- **Radial spotlight gradient behind the hero.** `[default]` Default "premium" filler. → Let type and composition carry the hero.
- **Tailwind default palette used verbatim** (`slate-900`, `indigo-500`, `gray-500` body). `[default]` Makes every site the same site. → Define tokens tuned to the brand.
- **Light gray body text on a light background** (`gray-400` on `#fff`). `[always]` Fails 4.5:1. → Darker neutral; demote with size or weight instead.
- **Random bright colors with no meaning.** `[always]` Color stops meaning anything. → One accent plus semantic colors.

## Typography

- **Inter, Roboto, Arial, system-ui, or Space Grotesk chosen without thought.** `[default]` → Pick a face with personality, or pick a neutral one on purpose and say why.
- **One word in the headline set in italic serif or gradient.** `[default]` The current AI headline cliché ("Build *beautiful* apps"). → Let the whole line carry the weight, or restructure the sentence.
- **Small uppercase eyebrow above every heading** ("FEATURES", "PRICING"). `[default]` Repeats what the heading already says. → Use eyebrows only where they add context the heading lacks.
- **Wide letter-spacing on uppercase labels everywhere.** `[default]` Fake polish. → Sentence case; keep tracking modest when caps are needed.
- **Staccato headlines with periods** ("Fast. Simple. Powerful."). `[default]` Every template headline. → Say one specific thing in a normal sentence.
- **Title Case and sentence case mixed on one page.** `[always]` Looks careless. → Pick one; sentence case is the safe default.
- **One-word last line in headings (widows).** `[always]` → `text-wrap: balance` on headings.
- **Too many sizes and weights on one screen.** `[always]` → 3–4 sizes; let weight do the work.
- **Body text too small to read.** `[always]` → 16px default, 14px floor for dense UI.
- **Oversized headlines that say nothing specific.** `[default]` → Make the headline smaller and the claim sharper.
- **Muted gray used so often it stops meaning "secondary."** `[always]` → Reserve muted text for truly secondary info.

## Layout

- **Card soup — everything wrapped in a card.** `[always]` A card implies a distinct thing. → Plain sections for text and lists; cards only for entities.
- **3-column grid of the same card repeated three or six times.** `[default]` → Vary size by priority, or use a list.
- **Centered hero, centered features, centered everything.** `[default]` Centered body text is hard to scan. → Left-align body; center only short display moments.
- **Image and text rows that swap sides all the way down (zig-zag).** `[default]` → Vary the structure; not every feature needs a picture.
- **Every section uses the same container width** (`max-w-7xl`). `[default]` Flattens rhythm. → Narrow for prose, wide for media, full-bleed for one or two moments.
- **Identical section spacing top to bottom.** `[always]` → Space by importance.
- **Bento grid used regardless of content.** `[default]` → Only when tiles truly differ in size and priority.
- **Dashboards as stacked widgets with no focal point.** `[always]` → One primary number or task leads.
- **`h-screen` / `100vh` hero.** `[always]` Breaks on mobile when the browser bar shows or hides. → `100svh` or `100dvh`, or content height.

## Borders, boxes, and containers

- **Colored left-edge bar as the only signal for active or selected state** (nav items, sidebar rows, tabs, cards, pills, tips). `[always]` Adjacent items each carrying an accent create competing hierarchies. → Background tint, icon state, or a weight shift. Reserve top or bottom borders for section grouping, not per-item status.
  The same bar in disguise counts too: `border-s-4`, `border-inline-start`, an inset shadow (`box-shadow: inset 3px 0 0 …`), or a `::before` strip pinned to the left edge.
- **Colored left stripe on callouts, alerts, notes, and blockquotes** (`border-l-4`). `[default]` The default "docs callout" look. → Tinted background plus an icon and a bold lead word; for quotes, use type (size, italic, hanging punctuation).
- **Colored top bar on cards** (`border-t-4`). `[default]` Same cliché rotated. → Let content or a small label signal category.
- **Border, ring, and shadow stacked on one element.** `[always]` Three edges fighting. → Pick one edge treatment.
- **Card inside a card inside a card.** `[always]` Nested containers with no new meaning. → Flatten; use spacing and dividers inside one surface.
- **Row dividers inside a bordered card.** `[default]` Double lines at every edge. → Dividers or a border, not both; or use spacing.
- **Gray border on every component.** `[default]` → Group with proximity and background tone.
- **Gradient or animated "beam" borders.** `[default]` → Solid 1px border at low contrast, or none.
- **Icon in a tinted square on every sidebar or list row.** `[default]` Visual noise at scale. → Bare icon; tint only the active row.
- **Same border radius on every element.** `[always]` Ignores nesting. → Concentric radii; vary radius by element size.
- **Colored ring around every avatar.** `[default]` → Plain avatar; ring only to mark a real state.

## Components

- **Icons in colored circles for every feature.** `[default]` → Plain icon, an illustration, or no icon.
- **Generic pill badges everywhere.** `[default]` → Badges only for real status or counts.
- **Heavy shadows used as fake depth.** `[always]` → Multiple low-opacity shadows or tone shifts.
- **Multiple CTAs of equal weight.** `[always]` → One primary; others ghost or link.
- **Fake chat or command-bar UI added because "AI products have those."** `[always]` → Only build UI the product actually uses.
- **Green circle checkmark on every list item.** `[default]` → Plain list, or checks only where they mean "included."
- **Shimmer, pulse, or bounce on the CTA.** `[default]` Begs for attention. → Strong static contrast is enough.
- **`kbd` shortcut hints for shortcuts that don't exist.** `[always]` → Show only working shortcuts.
- **Tooltips on everything.** `[default]` → Clear labels; tooltips for icon-only controls.
- **A toast for every action.** `[default]` → Show the result in place; toast only for background or undoable actions.
- **Modal to confirm a trivial or undoable action.** `[default]` → Do it and offer undo.
- **Spinner for loads under ~300ms.** `[default]` Flashes. → Delay the indicator; show it only if the load runs long.
- **Skeletons that don't match the real layout.** `[always]` Layout jumps when content lands. → Skeletons share the final dimensions.
- **Disabled submit button with no reason given.** `[always]` → Keep it enabled and show what is missing on submit, or explain inline.

## Icons

- **Icons from two or more sets on one screen.** `[always]` Stroke, corner, and fill styles clash. → One set.
- **Mixed stroke weights or sizes.** `[always]` → One stroke weight; a size scale of 16 / 20 / 24.
- **Icons centered on the line box instead of the text.** `[default]` They sit low or high. → Size to the text, nudge optically.
- **An icon next to every label.** `[default]` Icons stop helping when everything has one. → Icons only where they speed recognition.

## Marketing sections

- **Cookie-cutter structure: hero → features → testimonials → pricing → CTA.** `[default]` → Order sections by what this audience needs to believe.
- **"New → Announcing…" pill above the hero.** `[default]` → Only when there is real news, with a real link.
- **"Trusted by" logo row with placeholder or unearned logos.** `[always]` → Real customers or nothing.
- **Fake stats row** ("10k+ users · 99.9% uptime · 24/7 support"). `[always]` → Real numbers with a source, or cut the row.
- **Five-star testimonial cards with initials avatars.** `[default]` → Real quote, name, role, and photo; one strong quote beats six weak ones.
- **Monthly/yearly toggle with a "Save 20%" badge.** `[default]` → Fine when billing truly differs; otherwise show one price.
- **Product screenshot tilted in 3D perspective.** `[default]` Hides the product. → Show it flat and legible, cropped to the part that matters.
- **Fake code window or browser frame with three colored dots.** `[default]` → Show real code or the real product.
- **Logo marquee.** `[default]` → Static row; movement adds nothing.
- **FAQ accordion always at the bottom.** `[default]` → Answer objections where they arise.

## Decoration

- **Decorative blobs and shapes with no purpose.** `[default]` → Remove; let composition and type carry the page.
- **Floating dots, sparkles, waves, abstract SVG shapes as default polish.** `[default]` → Remove, or draw one shape that belongs to the brand.
- **Dot or grid background fading out from the center** (radial mask). `[default]` The current default backdrop. → Flat surface, or a texture tied to the product (a real map, real data).
- **Mesh gradients behind everything.** `[default]` → One gradient moment at most; flat elsewhere.
- **Grain overlay plus blur blobs together.** `[default]` Two atmosphere tricks fighting. → Keep one.
- **Spotlight that follows the cursor.** `[default]` Costs frames and means nothing. → Remove.
- **Emoji as a design system** (✨🚀 in headings and buttons). `[default]` → Real icons, or no icon. Keep emoji only for a playful brand that uses them in its own voice.
- **Glassmorphism stacked everywhere.** `[default]` → One translucent layer at most, with a solid fallback.
- **Noise textures everywhere.** `[default]` → Only as deliberate atmosphere.

If you cannot say what a decoration reinforces, remove it.

## Motion

- **Fade-up on scroll for every element.** `[default]` Delays reading and repeats on every block. → Reveal only key moments; most content should just be there.
- **Staggered reveal on every section.** `[default]` → Stagger once, where order means something.
- **Every card lifts on hover** (`-translate-y-1` + bigger shadow). `[default]` → Hover feedback only on things that are clickable, and keep it subtle.
- **Number count-up animations.** `[default]` Hides the number while it spins. → Show the final value.
- **Typing effect in the hero.** `[default]` Makes people wait to read. → Static text.
- **Parallax on scroll.** `[default]` → Only when depth carries meaning; respect reduced motion.
- **Infinite pulse, bounce, or ping on content or CTAs.** `[always]` Motion that never stops becomes noise. → Remove. Spinners and progress bars are exempt while the work runs.
- **Content hidden at `opacity: 0` until JS runs.** `[always]` Vanishes when JS fails or loads slowly. → Hide only under a `.js` class or use `@starting-style`.
- **Layout properties animated** (`width`, `height`, `top`, `left`, `margin`). `[always]` Janks. → `transform` for movement and size.
- **`transition: all`.** `[always]` → List exact properties.
- **Animation with no reduced-motion fallback.** `[always]` → `@media (prefers-reduced-motion: reduce)` that stops movement and decorative loops.

## Hierarchy

- **Everything has equal visual weight.** `[always]` → Pick the one element that matters; enlarge or darken it, demote the rest.
- **No obvious primary action.** `[always]` → One filled button per view.
- **Accent color on so many things that nothing stands out.** `[always]` → Accent only on the primary action and current state.
- **Cards, charts, filters, and tables all competing at once.** `[always]` → Lead with one; move filters to a quiet row; fold the rest below.

## Spacing and rhythm

- **Same padding on every component regardless of density.** `[always]` → Tight for dense controls, roomy for reading surfaces.
- **Same margin between every section regardless of importance.** `[always]` → More space before major sections, less within a group.
- **Random values that look "about right" but follow no system.** `[always]` → 4 or 8 base unit, from tokens.

## Product UI and dashboards

- **Designing every product like a marketing site.** `[always]` → Dense, calm, task-first: smaller type, fewer hero moments.
- **"+12.5% ↑" green delta badge on every KPI card.** `[default]` → Show change only where it matters, with the period it covers.
- **Charts everywhere when a number would do.** `[default]` → A plain number; chart only for trend or comparison.
- **Area charts with a gradient fill.** `[default]` → Plain line; fill only for stacked parts of a whole.
- **Zebra rows, borders, and hover highlight all on one table.** `[always]` → Pick one row separator.
- **Green online dot on every avatar.** `[default]` → Only where presence matters.
- **Search box in the top bar that does nothing.** `[always]` → Wire it up, or remove it.
- **Breadcrumbs in a two-level app.** `[default]` → A back link or a clear title.
- **Key data truncated with "…".** `[always]` → Wrap, widen, or show full value on focus.
- **Long forms dumped on one screen.** `[default]` → Group and step them.
- **Empty states that just say "No data."** `[always]` → Say what goes here and how to add it.
- **Missing hover, focus, active, or disabled states.** `[always]` → Build every state listed in `SKILL.md` → States.
- **Mobile layouts that are just narrower desktops.** `[always]` → Redesign: stack, collapse tables to rows, move secondary actions into a menu.

## Forms

- **Placeholder used as the label.** `[always]` Disappears on typing. → Label above the field.
- **Errors shown only as a red border.** `[always]` Color alone. → Message under the field that says how to fix it.
- **Errors shown only after submit.** `[default]` → Validate on blur for format, on submit for completeness.
- **No mark for required or optional fields.** `[always]` → Mark whichever is rarer.
- **Input height different from button height in the same row.** `[always]` → Share one control-height token.

## Content and copy

- **"Build smarter," "Unlock the power of AI," "Transform your workflow."** `[always]` → Name the task and the result.
- **Buzzwords: seamless, effortless, elevate, supercharge, unleash, next-gen, AI-powered.** `[always]` → Say what it actually does.
- **Value propositions that could belong to any startup.** `[always]` → Name the user, the job, and a number or detail only this product has.
- **Every feature described in the same sentence structure.** `[always]` → Vary length and shape; lead some with the result, some with the action.
- **Em dashes and three-item lists in every paragraph.** `[default]` A prose tell as strong as the purple gradient. → Periods and commas; lists of the length the content has.
- **Placeholder people and companies** (Acme Inc, Jane Cooper, John Doe, lorem ipsum). `[always]` → Real or realistic microcopy.
- **Invented testimonials, metrics, or customer counts.** `[always]` → Real ones, or leave the slot out.
- **"Get started free" and "Learn more" side by side at equal weight.** `[always]` → One button, one quiet link.

## Internationalization

- **Layout that only works with short English strings.** `[always]` German and Finnish run ~30% longer; labels clip or wrap badly. → Test with long strings; let buttons and tabs grow.
- **Physical `left` / `right` in layout CSS** (`ml-*`, `pl-*`, `border-l`, `left: 0`). `[default]` Breaks in right-to-left languages. → Logical properties: `margin-inline-start`, `border-inline-start`, Tailwind `ms-*` / `ps-*` / `border-s`.
- **Dates, numbers, and currency formatted by hand.** `[always]` → `Intl.DateTimeFormat`, `Intl.NumberFormat`.
- **Text baked into images.** `[always]` Can't translate or scale. → Live text over the image.

## Accessibility and code

- **`<div onClick>` where a `<button>` or `<a>` belongs.** `[always]` No keyboard or screen-reader support. → The native element.
- **Icon-only buttons with no `aria-label`.** `[always]` → Add one that names the action.
- **`outline: none` / `focus:outline-none` with no replacement ring.** `[always]` → `:focus-visible` ring with ≥ 3:1 contrast. Removing the outline only under `:focus:not(:focus-visible)` is fine.
- **Focus ring drawn only with `box-shadow`** (Tailwind `ring-*` alone). `[default]` Disappears in Windows high-contrast mode. → `outline` on `:focus-visible`, or add `outline: 2px solid transparent` under the ring.
- **Content that only appears on hover.** `[always]` Unreachable on touch and keyboard. → Show it always, or on focus and tap too.
- **Images without `width` and `height`.** `[always]` Layout shifts as they load. → Set both, or `aspect-ratio`.
- **Hardcoded color, spacing, and radius values.** `[always]` → Tokens.
- **`!important` and `z-index: 9999`.** `[always]` → Fix the cascade; use a z-index scale. `!important` inside a `prefers-reduced-motion` block is fine.
- **Dark mode made by inverting colors, or white text on pure black.** `[always]` → Design dark tokens; lower contrast slightly and lift surfaces with tone.
- **Inconsistent component styles across screens.** `[always]` → One component per job, reused.
- **Broken or missing dark mode when the product has one.** `[always]` → Check every screen in both themes.

## Short rule of thumb

If the UI has a purple gradient hero, a pill above the headline, one italic word in the heading, card soup, Inter everywhere, icons in colored circles, left-border accents, fade-up on every block, fake stats, and centered everything, it looks polished but is forgettable after five seconds. Correct it.
