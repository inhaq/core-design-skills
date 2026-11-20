// Focus and click handling as product code writes it. The checker must report nothing here.
// Cases sit 4+ lines apart so each focus exemption is tested on its own.
import { useFlag } from "@unleash/proxy-client-react";

export function Toolbar({ onClose }: { onClose: () => void }) {
  const showBeta = useFlag("beta");
  return (
    <main id="main" tabIndex={-1} className="outline-none">
      <a href="/w/acme/settings">Settings</a>
      <div role="button" tabIndex={0} onClick={onClose} onKeyDown={onClose}>Close</div>
      <div className="scrim" aria-hidden="true" onClick={onClose} />

      <button className="rounded-md focus:ring-2 focus:ring-accent focus:outline-none">Save</button>



      <input
        className={cn(
          "h-9 rounded-md border outline-none",
          "focus-visible:ring-2 focus-visible:ring-accent",
        )}
      />
      {showBeta && <span>Beta</span>}
    </main>
  );
}
