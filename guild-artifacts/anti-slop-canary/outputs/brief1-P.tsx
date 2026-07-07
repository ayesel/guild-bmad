import React, { useState } from "react";
import { Check, Minus, Plus, ArrowRight } from "lucide-react";

/**
 * Notely — Pricing
 * Warm, editorial, confident. Paper tones, serif display type,
 * one rationed moment of personality (the hand-drawn underline in the hero).
 */

const SERIF = "[font-family:Georgia,'Iowan_Old_Style','Times_New_Roman',serif]";

type Plan = {
  name: string;
  price: string;
  cadence: string;
  blurb: string;
  features: string[];
  cta: string;
  highlighted?: boolean;
};

const PLANS: Plan[] = [
  {
    name: "Free",
    price: "$0",
    cadence: "forever",
    blurb: "For the napkin-sketch stage. Every good archive starts somewhere.",
    features: [
      "Up to 200 notes",
      "Full-text search",
      "Web clipper",
      "Sync across 2 devices",
    ],
    cta: "Start writing",
  },
  {
    name: "Pro",
    price: "$8",
    cadence: "per month, billed yearly",
    blurb: "For people whose notes are doing real work — research, drafts, a second brain.",
    features: [
      "Unlimited notes & devices",
      "Version history, 12 months",
      "Backlinks & graph view",
      "Offline mode",
      "PDF & Markdown export",
      "Priority support",
    ],
    cta: "Go Pro",
    highlighted: true,
  },
  {
    name: "Team",
    price: "$14",
    cadence: "per member / month",
    blurb: "Shared context for small teams. One quiet, well-kept source of truth.",
    features: [
      "Everything in Pro",
      "Shared workspaces",
      "Granular permissions",
      "Admin console & SSO",
      "Audit log",
    ],
    cta: "Bring your team",
  },
];

const FAQS: { q: string; a: string }[] = [
  {
    q: "Can I switch plans later?",
    a: "Any time. Upgrades apply immediately and we prorate the difference; downgrades take effect at the end of your billing period. Your notes never move — only the ceiling does.",
  },
  {
    q: "What happens to my notes if I cancel?",
    a: "They stay yours. Cancelled accounts drop to the Free tier with read access to everything, and you can export the whole archive to Markdown in one click, forever.",
  },
  {
    q: "Do you offer student or nonprofit discounts?",
    a: "Yes — 50% off Pro for students and educators, and free Team plans for registered nonprofits under ten seats. Write to us from your institutional address.",
  },
];

function Underline() {
  // The one rationed moment of personality: a hand-drawn stroke
  // beneath the key phrase in the hero. Nowhere else.
  return (
    <svg
      aria-hidden="true"
      viewBox="0 0 220 14"
      className="absolute -bottom-2 left-0 w-full"
      preserveAspectRatio="none"
    >
      <path
        d="M3 10 C 45 3, 90 12, 130 7 S 200 4, 217 8"
        fill="none"
        stroke="#B4460F"
        strokeWidth="4"
        strokeLinecap="round"
      />
    </svg>
  );
}

function PlanCard({ plan }: { plan: Plan }) {
  const dark = plan.highlighted;
  return (
    <div
      className={
        dark
          ? "flex flex-col rounded-lg bg-[#1E1913] px-8 py-10 text-[#F7F1E5] shadow-[0_24px_48px_-16px_rgba(30,25,19,0.35)] lg:-my-6"
          : "flex flex-col rounded-lg border border-[#E3D9C6] bg-transparent px-8 py-10 text-[#1E1913]"
      }
    >
      <div className="flex items-baseline justify-between">
        <h3 className={`${SERIF} text-xl`}>{plan.name}</h3>
        {dark && (
          <span className="text-[11px] font-semibold uppercase tracking-[0.18em] text-[#E8A87C]">
            Most kept
          </span>
        )}
      </div>

      <p
        className={`mt-3 text-sm leading-relaxed ${
          dark ? "text-[#C9BFAC]" : "text-[#6B6152]"
        }`}
      >
        {plan.blurb}
      </p>

      <div className="mt-8 flex items-baseline gap-2">
        <span className={`${SERIF} text-5xl tracking-tight`}>{plan.price}</span>
        <span
          className={`text-sm ${dark ? "text-[#C9BFAC]" : "text-[#6B6152]"}`}
        >
          {plan.cadence}
        </span>
      </div>

      <a
        href="#"
        className={
          dark
            ? "mt-8 inline-flex items-center justify-center gap-2 rounded-md bg-[#B4460F] px-5 py-3 text-sm font-medium text-[#FBF6EC] transition-colors duration-200 ease-out hover:bg-[#983A0C]"
            : "mt-8 inline-flex items-center justify-center gap-2 rounded-md border border-[#1E1913] px-5 py-3 text-sm font-medium text-[#1E1913] transition-colors duration-200 ease-out hover:bg-[#1E1913] hover:text-[#F7F1E5]"
        }
      >
        {plan.cta}
        <ArrowRight className="h-4 w-4" strokeWidth={1.75} />
      </a>

      <hr
        className={`my-8 border-t ${
          dark ? "border-[#3A3226]" : "border-[#E3D9C6]"
        }`}
      />

      <ul className="flex flex-col gap-3">
        {plan.features.map((f) => (
          <li key={f} className="flex items-start gap-3 text-sm leading-6">
            <Check
              className={`mt-1 h-4 w-4 shrink-0 ${
                dark ? "text-[#E8A87C]" : "text-[#B4460F]"
              }`}
              strokeWidth={2}
            />
            <span className={dark ? "text-[#EDE5D4]" : "text-[#3C352A]"}>
              {f}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function FaqRow({
  item,
  open,
  onToggle,
}: {
  item: { q: string; a: string };
  open: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="border-t border-[#E3D9C6]">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-6 py-6 text-left"
      >
        <span className={`${SERIF} text-lg text-[#1E1913]`}>{item.q}</span>
        {open ? (
          <Minus className="h-5 w-5 shrink-0 text-[#B4460F]" strokeWidth={1.75} />
        ) : (
          <Plus className="h-5 w-5 shrink-0 text-[#6B6152]" strokeWidth={1.75} />
        )}
      </button>
      {open && (
        <p className="max-w-2xl pb-7 text-[15px] leading-relaxed text-[#6B6152]">
          {item.a}
        </p>
      )}
    </div>
  );
}

export default function Pricing() {
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  return (
    <main className="min-h-screen bg-[#FBF6EC] antialiased">
      {/* Top bar — quiet wordmark, nothing competing with the hero */}
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-7">
        <a href="#" className={`${SERIF} text-2xl tracking-tight text-[#1E1913]`}>
          Notely<span className="text-[#B4460F]">.</span>
        </a>
        <nav className="flex items-center gap-8 text-sm text-[#3C352A]">
          <a href="#" className="hover:text-[#1E1913]">
            Product
          </a>
          <a href="#" className="hover:text-[#1E1913]">
            Changelog
          </a>
          <a
            href="#"
            className="rounded-md border border-[#1E1913] px-4 py-2 font-medium text-[#1E1913] transition-colors duration-200 ease-out hover:bg-[#1E1913] hover:text-[#F7F1E5]"
          >
            Sign in
          </a>
        </nav>
      </header>

      {/* Hero — asymmetric, editorial, left-set like a magazine deck */}
      <section className="mx-auto max-w-6xl px-6 pb-20 pt-16 lg:pt-24">
        <p className="text-xs font-semibold uppercase tracking-[0.22em] text-[#6B6152]">
          Pricing
        </p>
        <h1
          className={`${SERIF} mt-5 max-w-3xl text-5xl leading-[1.08] tracking-tight text-[#1E1913] lg:text-[64px]`}
        >
          Pay for the notes{" "}
          <span className="relative inline-block whitespace-nowrap">
            worth keeping
            <Underline />
          </span>
          .
        </h1>
        <div className="mt-8 flex max-w-3xl flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <p className="max-w-md text-lg leading-relaxed text-[#6B6152]">
            Notely is free for as long as you like. Upgrade when your archive
            starts pulling its weight — no seats math, no surprise invoices.
          </p>
          <p className="shrink-0 text-sm text-[#6B6152]">
            All plans include a 30-day money-back promise.
          </p>
        </div>
      </section>

      {/* Plans */}
      <section className="mx-auto max-w-6xl px-6 pb-28">
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3 lg:gap-8">
          {PLANS.map((plan) => (
            <PlanCard key={plan.name} plan={plan} />
          ))}
        </div>
        <p className="mt-10 text-center text-sm text-[#6B6152]">
          Prices in USD. Monthly billing available at $10 (Pro) and $17 (Team).
        </p>
      </section>

      {/* FAQ teaser */}
      <section className="border-t border-[#E3D9C6] bg-[#F5EEDF]">
        <div className="mx-auto grid max-w-6xl grid-cols-1 gap-12 px-6 py-20 lg:grid-cols-[1fr_1.6fr] lg:gap-20">
          <div>
            <h2 className={`${SERIF} text-3xl tracking-tight text-[#1E1913]`}>
              Fair questions
            </h2>
            <p className="mt-4 text-[15px] leading-relaxed text-[#6B6152]">
              The short version of the fine print. For the long version —
              billing, exports, security — the full FAQ has you covered.
            </p>
            <a
              href="#"
              className="mt-6 inline-flex items-center gap-2 text-sm font-medium text-[#B4460F] hover:text-[#983A0C]"
            >
              Read the full FAQ
              <ArrowRight className="h-4 w-4" strokeWidth={1.75} />
            </a>
          </div>

          <div className="border-b border-[#E3D9C6]">
            {FAQS.map((item, i) => (
              <FaqRow
                key={item.q}
                item={item}
                open={openFaq === i}
                onToggle={() => setOpenFaq(openFaq === i ? null : i)}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Footer strip */}
      <footer className="mx-auto flex max-w-6xl flex-col items-start justify-between gap-4 px-6 py-10 text-sm text-[#6B6152] lg:flex-row lg:items-center">
        <p>
          <span className={`${SERIF} text-[#1E1913]`}>Notely</span> — notes that
          stay put.
        </p>
        <p>© 2026 Notely, Inc. · Terms · Privacy</p>
      </footer>
    </main>
  );
}
