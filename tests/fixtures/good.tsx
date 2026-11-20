// Patterns that look like tells but are fine. outline: none in a comment is not code.
export function Field({ value }: { value: string }) {
  return (
    <div className="flex items-center rounded-lg border focus-within:ring-2 focus-within:ring-accent">
      <input
        value={value}
        placeholder="e.g. Acme Analytics"
        className="h-11 bg-transparent focus:outline-none"
      />
      <span className="h-3 w-16 rounded bg-surface-2 animate-pulse" />
      <span className="size-1.5 rounded-full bg-muted animate-bounce" aria-hidden="true" />
      <p className="ml-4">Physical spacing is only flagged with --rtl.</p>
    </div>
  );
}
