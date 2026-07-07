import React from "react";
import { Check, Minus, ArrowRight } from "lucide-react";

/**
 * Notely — Pricing
 * Editorial, ledger-style pricing page. Warm paper ground, ink typography,
 * a single deep-green accent. Columns are divided by rules, not floated
 * cards; the Pro tier is highlighted by inverting its panel to ink.
 */

const serif: React.CSSProperties = {
  fontFamily: 'Georgia, "Iowan Old Style", "Times New Roman", serif',
};

type Feature = { label: string; included: boolean };

type Plan = {
  name: string;
  price: string;
  period: string;
  blurb: string;
  cta: string;
  highlighted: boolean;
  features: Feature[];
};

const PLANS: Plan[] = [
  {
    name: "Free",
    price: "$0",
    period: "forever",
    blurb: "For getting your first thousand thoughts out of your head.",
    cta: "Start writing",
    highlighted: false,
    features: [
      { label: "Unlimited notes on one device", included: true },
      { label: "Markdown editor with slash commands", included: true },
      { label: "Full-text search", included: true },
      { label: "Sync across devices", included: false },
      { label: "Version history", included: false },
      { label: "Shared workspaces", included: false },
    ],
  },
  {
    name: "Pro",
    price: "$8",
    period: "per month, billed yearly",
    blurb: "For people whose notes are their second brain, not a junk drawer.",
    cta: "Upgrade to Pro",
    highlighted: true,
    features: [
      { label: "Everything in Free", included: true },
      { label: "Sync across unlimited devices", included: true },
      { label: "30-day version history", included: true },
      { label: "Offline access on mobile", included: true },
      { label: "Web clipper and email-to-note", included: true },
      { label: "Shared workspaces", included: false },
    ],
  },
  {
    name: "Team",
    price: "$14",
    period: "per member / month",
    blurb: "For teams who would rather share notes than schedule meetings.",
    cta: "Start a team trial",
    highlighted: false,
    features: [
      { label: "Everything in Pro", included: true },
      { label: "Shared workspaces and permissions", included: true },
      { label: "Unlimited version history", included: true },
      { label: "Admin console and SSO", included: true },
      { label: "Priority support", included: true },
      { label: "Audit log export", included: true },
    ],
  },
];

const FAQS: { q: string; a: string }[] = [
  {
    q: "Can I switch plans later?",
    a: "Any time. Upgrades take effect immediately; downgrades apply at the end of your billing period, and your notes are never locked away.",
  },
  {
    q: "What happens to my notes if I cancel?",
    a: "They stay yours. Cancelled accounts drop to the Free plan with everything intact, and you can export all notes as Markdown whenever you like.",
  },
  {
    q: "Do you offer education or nonprofit discounts?",
    a: "Yes — students, educators, and registered nonprofits get 40% off Pro and Team. Write to us from your institutional email.",
  },
];

function PlanColumn({ plan }: { plan: Plan }) {
  const inverted = plan.highlighted;
  return (
    <div
      className={
        inverted
          ? "flex flex-col bg-stone-900 text-stone-100 px-8 py-10"
          : "flex flex-col px-8 py-10"
      }
    >
      <div className="flex items-baseline justify-between">
        <h3
          style={serif}
          className={
            inverted
              ? "text-2xl text-stone-50"
              : "text-2xl text-stone-900"
          }
        >
          {plan.name}
        </h3>
        {inverted && (
          <span className="text-xs uppercase tracking-[0.2em] text-emerald-400">
            Most popular
          </span>
        )}
      </div>

      <p
        className={
          inverted
            ? "mt-3 text-sm leading-relaxed text-stone-400"
            : "mt-3 text-sm leading-relaxed text-stone-600"
        }
      >
        {plan.blurb}
      </p>

      <div className="mt-8 flex items-baseline gap-2">
        <span
          style={serif}
          className={
            inverted ? "text-5xl text-stone-50" : "text-5xl text-stone-900"
          }
        >
          {plan.price}
        </span>
        <span
          className={
            inverted ? "text-sm text-stone-400" : "text-sm text-stone-500"
          }
        >
          {plan.period}
        </span>
      </div>

      <a
        href="#signup"
        className={
          inverted
            ? "mt-8 inline-flex items-center justify-center gap-2 bg-emerald-500 px-5 py-3 text-sm font-medium text-stone-950 transition-colors duration-150 ease-out hover:bg-emerald-400"
            : "mt-8 inline-flex items-center justify-center gap-2 border border-stone-900 px-5 py-3 text-sm font-medium text-stone-900 transition-colors duration-150 ease-out hover:bg-stone-900 hover:text-stone-50"
        }
      >
        {plan.cta}
        <ArrowRight size={16} strokeWidth={1.75} aria-hidden="true" />
      </a>

      <ul
        className={
          inverted
            ? "mt-10 space-y-3 border-t border-stone-700 pt-8"
            : "mt-10 space-y-3 border-t border-stone-300 pt-8"
        }
      >
        {plan.features.map((f) => (
          <li key={f.label} className="flex items-start gap-3 text-sm">
            {f.included ? (
              <Check
                size={16}
                strokeWidth={2}
                aria-hidden="true"
                className={
                  inverted
                    ? "mt-0.5 shrink-0 text-emerald-400"
                    : "mt-0.5 shrink-0 text-emerald-700"
                }
              />
            ) : (
              <Minus
                size={16}
                strokeWidth={2}
                aria-hidden="true"
                className={
                  inverted
                    ? "mt-0.5 shrink-0 text-stone-600"
                    : "mt-0.5 shrink-0 text-stone-400"
                }
              />
            )}
            <span
              className={
                f.included
                  ? inverted
                    ? "text-stone-200"
                    : "text-stone-800"
                  : inverted
                  ? "text-stone-500"
                  : "text-stone-400"
              }
            >
              {f.label}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default function PricingPage() {
  return (
    <main className="min-h-screen bg-[#FAF7F1] text-stone-900 antialiased">
      {/* Masthead */}
      <header className="border-b border-stone-300">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <a href="#" style={serif} className="text-xl tracking-tight">
            Notely
          </a>
          <nav aria-label="Primary" className="flex items-center gap-8 text-sm">
            <a href="#" className="text-stone-600 hover:text-stone-900">
              Product
            </a>
            <a href="#" className="text-stone-900 underline underline-offset-4">
              Pricing
            </a>
            <a href="#" className="text-stone-600 hover:text-stone-900">
              Changelog
            </a>
            <a
              href="#signup"
              className="border border-stone-900 px-4 py-2 text-stone-900 transition-colors duration-150 ease-out hover:bg-stone-900 hover:text-stone-50"
            >
              Sign in
            </a>
          </nav>
        </div>
      </header>

      {/* Hero */}
      <section className="border-b border-stone-300">
        <div className="mx-auto grid max-w-6xl grid-cols-12 gap-8 px-6 py-20">
          <div className="col-span-7">
            <h1
              style={serif}
              className="text-6xl leading-[1.05] tracking-tight text-stone-900"
            >
              Pay for the notes
              <br />
              you keep, not the
              <br />
              <em className="text-emerald-800">app you open.</em>
            </h1>
          </div>
          <div className="col-span-4 col-start-9 flex flex-col justify-end">
            <p className="text-base leading-relaxed text-stone-600">
              Notely starts free and stays honest. One flat price when you
              outgrow one device, one flat price when your whole team moves in.
              No per-seat surprises, no feature ransom.
            </p>
            <p className="mt-4 text-sm text-stone-500">
              Every paid plan includes a 14-day trial. No card required.
            </p>
          </div>
        </div>
      </section>

      {/* Plans — a single ruled ledger, columns divided by hairlines */}
      <section aria-labelledby="plans-heading" className="border-b border-stone-300">
        <h2 id="plans-heading" className="sr-only">
          Plans and pricing
        </h2>
        <div className="mx-auto max-w-6xl px-6 py-16">
          <div className="grid grid-cols-3 divide-x divide-stone-300 border border-stone-300 bg-[#FFFDF9]">
            {PLANS.map((plan) => (
              <PlanColumn key={plan.name} plan={plan} />
            ))}
          </div>
          <p className="mt-6 text-center text-sm text-stone-500">
            Prices in USD. Yearly billing shown; monthly billing available at
            checkout.
          </p>
        </div>
      </section>

      {/* FAQ teaser */}
      <section aria-labelledby="faq-heading">
        <div className="mx-auto grid max-w-6xl grid-cols-12 gap-8 px-6 py-20">
          <div className="col-span-4">
            <h2 id="faq-heading" style={serif} className="text-3xl text-stone-900">
              Asked, answered.
            </h2>
            <a
              href="#faq"
              className="mt-4 inline-flex items-center gap-2 text-sm font-medium text-emerald-800 hover:text-emerald-700"
            >
              Read the full FAQ
              <ArrowRight size={16} strokeWidth={1.75} aria-hidden="true" />
            </a>
          </div>
          <div className="col-span-8">
            <dl className="divide-y divide-stone-300 border-t border-b border-stone-300">
              {FAQS.map((item) => (
                <div key={item.q} className="grid grid-cols-8 gap-6 py-6">
                  <dt style={serif} className="col-span-3 text-lg text-stone-900">
                    {item.q}
                  </dt>
                  <dd className="col-span-5 text-sm leading-relaxed text-stone-600">
                    {item.a}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        </div>
      </section>

      {/* Footer strip */}
      <footer className="border-t border-stone-300">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-8 text-sm text-stone-500">
          <p>© 2026 Notely, Inc.</p>
          <p>
            Questions about plans?{" "}
            <a
              href="mailto:hello@notely.app"
              className="text-stone-700 underline underline-offset-4 hover:text-stone-900"
            >
              hello@notely.app
            </a>
          </p>
        </div>
      </footer>
    </main>
  );
}
