import React, { useState } from "react";
import { Check, Minus, ArrowRight, ChevronDown, PenLine } from "lucide-react";

type Plan = {
  name: string;
  price: string;
  cadence: string;
  blurb: string;
  cta: string;
  highlighted: boolean;
  features: { label: string; included: boolean }[];
};

const PLANS: Plan[] = [
  {
    name: "Free",
    price: "$0",
    cadence: "forever",
    blurb: "For getting your thoughts out of your head and into one place.",
    cta: "Start writing",
    highlighted: false,
    features: [
      { label: "Up to 200 notes", included: true },
      { label: "2 notebooks", included: true },
      { label: "Full-text search", included: true },
      { label: "Sync across 2 devices", included: true },
      { label: "Version history", included: false },
      { label: "Shared notebooks", included: false },
    ],
  },
  {
    name: "Pro",
    price: "$8",
    cadence: "per month, billed yearly",
    blurb: "For people whose notes are their second brain, not a junk drawer.",
    cta: "Go Pro",
    highlighted: true,
    features: [
      { label: "Unlimited notes & notebooks", included: true },
      { label: "Unlimited device sync", included: true },
      { label: "30-day version history", included: true },
      { label: "Offline access", included: true },
      { label: "PDF & Markdown export", included: true },
      { label: "Shared notebooks", included: false },
    ],
  },
  {
    name: "Team",
    price: "$14",
    cadence: "per member / month",
    blurb: "For teams that want one shared memory instead of forty DM threads.",
    cta: "Start a team trial",
    highlighted: false,
    features: [
      { label: "Everything in Pro", included: true },
      { label: "Shared notebooks & spaces", included: true },
      { label: "Comments & @mentions", included: true },
      { label: "Admin controls & SSO", included: true },
      { label: "90-day version history", included: true },
      { label: "Priority support", included: true },
    ],
  },
];

const FAQS: { q: string; a: string }[] = [
  {
    q: "Can I switch plans later?",
    a: "Anytime. Upgrades take effect immediately and we prorate the difference; downgrades apply at the end of your current billing period. Your notes are never locked behind a plan change.",
  },
  {
    q: "What happens to my notes if I cancel?",
    a: "They stay yours. Your account drops back to the Free plan, everything remains readable, and you can export all notes as Markdown or PDF at any time.",
  },
  {
    q: "Do you offer discounts for students or nonprofits?",
    a: "Yes — verified students get Pro at 50% off, and registered nonprofits get 30% off Team. Write to us from your institutional email and we'll set it up.",
  },
];

function PlanCard({ plan }: { plan: Plan }) {
  return (
    <div
      className={
        "relative flex flex-col rounded-2xl border p-8 " +
        (plan.highlighted
          ? "border-indigo-500 bg-indigo-50/50 shadow-lg shadow-indigo-100"
          : "border-slate-200 bg-white")
      }
    >
      {plan.highlighted && (
        <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-indigo-600 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-white">
          Most popular
        </span>
      )}

      <h3 className="text-lg font-semibold text-slate-900">{plan.name}</h3>
      <p className="mt-2 min-h-[3rem] text-sm leading-relaxed text-slate-600">
        {plan.blurb}
      </p>

      <div className="mt-6 flex items-baseline gap-2">
        <span className="text-4xl font-bold tracking-tight text-slate-900">
          {plan.price}
        </span>
        <span className="text-sm text-slate-500">{plan.cadence}</span>
      </div>

      <button
        type="button"
        className={
          "mt-6 inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-semibold transition-colors " +
          (plan.highlighted
            ? "bg-indigo-600 text-white hover:bg-indigo-700"
            : "border border-slate-300 bg-white text-slate-900 hover:bg-slate-50")
        }
      >
        {plan.cta}
        <ArrowRight className="h-4 w-4" aria-hidden="true" />
      </button>

      <ul className="mt-8 flex flex-col gap-3 border-t border-slate-200 pt-6">
        {plan.features.map((feature) => (
          <li key={feature.label} className="flex items-start gap-3 text-sm">
            {feature.included ? (
              <Check
                className="mt-0.5 h-4 w-4 shrink-0 text-indigo-600"
                aria-hidden="true"
              />
            ) : (
              <Minus
                className="mt-0.5 h-4 w-4 shrink-0 text-slate-300"
                aria-hidden="true"
              />
            )}
            <span
              className={feature.included ? "text-slate-700" : "text-slate-400"}
            >
              {feature.label}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function FaqItem({
  faq,
  open,
  onToggle,
}: {
  faq: { q: string; a: string };
  open: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="border-b border-slate-200 py-5 last:border-b-0">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-4 text-left"
      >
        <span className="text-base font-medium text-slate-900">{faq.q}</span>
        <ChevronDown
          className={
            "h-5 w-5 shrink-0 text-slate-400 transition-transform " +
            (open ? "rotate-180" : "")
          }
          aria-hidden="true"
        />
      </button>
      {open && (
        <p className="mt-3 pr-9 text-sm leading-relaxed text-slate-600">
          {faq.a}
        </p>
      )}
    </div>
  );
}

export default function PricingPage() {
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  return (
    <main className="min-h-screen bg-slate-50 text-slate-900">
      {/* Hero */}
      <section className="mx-auto max-w-5xl px-6 pb-16 pt-24 text-center">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-medium text-slate-600">
          <PenLine className="h-3.5 w-3.5 text-indigo-600" aria-hidden="true" />
          Notely pricing
        </div>
        <h1 className="text-4xl font-bold tracking-tight sm:text-5xl">
          Pay for the notes you keep,
          <br className="hidden sm:block" /> not the app you open
        </h1>
        <p className="mx-auto mt-5 max-w-2xl text-lg leading-relaxed text-slate-600">
          Start free and take notes forever. Upgrade when your notebook becomes
          the place you actually think — no feature roulette, no surprise
          limits mid-sentence.
        </p>
      </section>

      {/* Plans */}
      <section
        aria-label="Pricing plans"
        className="mx-auto max-w-5xl px-6 pb-24"
      >
        <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
          {PLANS.map((plan) => (
            <PlanCard key={plan.name} plan={plan} />
          ))}
        </div>
        <p className="mt-6 text-center text-sm text-slate-500">
          All paid plans include a 14-day free trial. No credit card required.
        </p>
      </section>

      {/* FAQ teaser */}
      <section aria-label="Frequently asked questions" className="bg-white">
        <div className="mx-auto max-w-3xl px-6 py-20">
          <h2 className="text-2xl font-bold tracking-tight">
            Questions, answered
          </h2>
          <p className="mt-2 text-sm text-slate-600">
            The three we hear most often. The rest live in our help center.
          </p>
          <div className="mt-8">
            {FAQS.map((faq, index) => (
              <FaqItem
                key={faq.q}
                faq={faq}
                open={openFaq === index}
                onToggle={() =>
                  setOpenFaq(openFaq === index ? null : index)
                }
              />
            ))}
          </div>
          <a
            href="#faq"
            className="mt-8 inline-flex items-center gap-2 text-sm font-semibold text-indigo-600 hover:text-indigo-700"
          >
            Browse the full FAQ
            <ArrowRight className="h-4 w-4" aria-hidden="true" />
          </a>
        </div>
      </section>
    </main>
  );
}
