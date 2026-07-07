import React from "react";
import { Footprints, Flame, Timer, ArrowUpRight } from "lucide-react";

/**
 * Stride — home dashboard
 *
 * Design notes: warm paper ground, ink typography set in a serif (editorial,
 * not app-generic), hairline rules instead of drop shadows, a ledger-style
 * stat column rather than a symmetric card grid. The single hero moment is
 * the streak block — one oversized italic numeral on ink. Everything else
 * stays quiet on purpose.
 */

type Stat = {
  id: string;
  label: string;
  value: string;
  unit: string;
  note: string;
  icon: React.ComponentType<{ size?: number | string; className?: string; strokeWidth?: number | string }>;
};

type DayActivity = {
  day: string;
  minutes: number;
};

const STATS: Stat[] = [
  {
    id: "steps",
    label: "Steps",
    value: "9,482",
    unit: "of 10,000",
    note: "518 to go — an easy lap around the block",
    icon: Footprints,
  },
  {
    id: "calories",
    label: "Calories",
    value: "612",
    unit: "kcal burned",
    note: "Ahead of your usual Tuesday by 9%",
    icon: Flame,
  },
  {
    id: "active",
    label: "Active minutes",
    value: "47",
    unit: "of 60 min",
    note: "Morning run did most of the work",
    icon: Timer,
  },
];

const WEEK: DayActivity[] = [
  { day: "Mon", minutes: 38 },
  { day: "Tue", minutes: 52 },
  { day: "Wed", minutes: 24 },
  { day: "Thu", minutes: 61 },
  { day: "Fri", minutes: 45 },
  { day: "Sat", minutes: 74 },
  { day: "Sun", minutes: 47 },
];

const STREAK_DAYS = 14;

function formatToday(): string {
  return new Intl.DateTimeFormat("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  }).format(new Date());
}

function greetingForHour(hour: number): string {
  if (hour < 5) return "Up early";
  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
}

export default function Dashboard() {
  const today = formatToday();
  const greeting = greetingForHour(new Date().getHours());

  const maxMinutes = Math.max(...WEEK.map((d) => d.minutes));
  const weekTotal = WEEK.reduce((sum, d) => sum + d.minutes, 0);

  return (
    <div className="min-h-screen bg-[#faf6ee] text-stone-900 antialiased">
      <main className="mx-auto max-w-5xl px-6 pb-24 pt-14 sm:px-10">
        {/* ------------------------------------------------------------- */}
        {/* Header                                                        */}
        {/* ------------------------------------------------------------- */}
        <header className="border-b border-stone-900/15 pb-10">
          <p className="text-[11px] font-medium uppercase tracking-[0.22em] text-stone-500">
            Stride · {today}
          </p>
          <h1 className="mt-4 font-serif text-4xl leading-[1.08] tracking-tight text-stone-900 sm:text-5xl">
            {greeting}, Maya.
          </h1>
          <p className="mt-3 max-w-md font-serif text-lg italic text-stone-500">
            Today is quietly adding up — keep it moving.
          </p>
        </header>

        {/* ------------------------------------------------------------- */}
        {/* Stats: ledger column + streak hero                            */}
        {/* ------------------------------------------------------------- */}
        <section
          aria-label="Today's stats"
          className="grid grid-cols-1 gap-x-14 border-b border-stone-900/15 md:grid-cols-5"
        >
          {/* Ledger of three quiet stats */}
          <div className="md:col-span-3">
            <ul className="divide-y divide-stone-900/10">
              {STATS.map((stat) => {
                const Icon = stat.icon;
                return (
                  <li
                    key={stat.id}
                    className="flex items-baseline justify-between gap-6 py-7"
                  >
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 text-stone-500">
                        <Icon size={14} strokeWidth={1.75} className="shrink-0" />
                        <span className="text-[11px] font-medium uppercase tracking-[0.18em]">
                          {stat.label}
                        </span>
                      </div>
                      <p className="mt-2 text-sm leading-relaxed text-stone-500">
                        {stat.note}
                      </p>
                    </div>
                    <div className="shrink-0 text-right">
                      <span className="font-serif text-4xl tabular-nums tracking-tight text-stone-900">
                        {stat.value}
                      </span>
                      <span className="mt-1 block text-xs text-stone-400">
                        {stat.unit}
                      </span>
                    </div>
                  </li>
                );
              })}
            </ul>
          </div>

          {/* THE hero moment: the streak, oversized on ink */}
          <div className="md:col-span-2 md:border-l md:border-stone-900/15 md:pl-14">
            <div className="my-7 bg-stone-900 px-8 py-9 text-[#faf6ee] md:my-0 md:mt-7">
              <p className="text-[11px] font-medium uppercase tracking-[0.22em] text-stone-400">
                Streak
              </p>
              <p className="mt-1 font-serif text-[7rem] italic leading-none tracking-tight text-[#e8590c]">
                {STREAK_DAYS}
              </p>
              <p className="mt-2 font-serif text-lg text-[#faf6ee]">
                days in a row
              </p>
              <p className="mt-4 border-t border-white/15 pt-4 text-sm leading-relaxed text-stone-400">
                Your longest yet. One more and it&rsquo;s a personal record
                that started on a rainy Monday.
              </p>
            </div>
          </div>
        </section>

        {/* ------------------------------------------------------------- */}
        {/* Weekly activity                                               */}
        {/* ------------------------------------------------------------- */}
        <section aria-label="This week's activity" className="pt-12">
          <div className="flex flex-wrap items-baseline justify-between gap-4">
            <h2 className="font-serif text-2xl tracking-tight text-stone-900">
              This week
            </h2>
            <p className="text-sm text-stone-500">
              <span className="font-medium tabular-nums text-stone-900">
                {weekTotal}
              </span>{" "}
              active minutes ·{" "}
              <a
                href="#history"
                className="inline-flex items-center gap-1 font-medium text-[#c2410c] underline decoration-[#c2410c]/30 underline-offset-4 transition-colors duration-200 ease-out hover:decoration-[#c2410c]"
              >
                Full history
                <ArrowUpRight size={14} strokeWidth={2} />
              </a>
            </p>
          </div>

          <div className="mt-8">
            <div
              role="img"
              aria-label={`Bar chart of active minutes this week: ${WEEK.map(
                (d) => `${d.day} ${d.minutes} minutes`
              ).join(", ")}.`}
              className="flex h-44 items-end gap-3 border-b border-stone-900/20 sm:gap-5"
            >
              {WEEK.map((d) => {
                const isBest = d.minutes === maxMinutes;
                return (
                  <div
                    key={d.day}
                    className="group relative flex h-full flex-1 items-end"
                  >
                    {isBest && (
                      <span className="absolute -top-6 left-1/2 -translate-x-1/2 whitespace-nowrap text-xs font-medium tabular-nums text-[#c2410c]">
                        {d.minutes} min
                      </span>
                    )}
                    <div
                      className={
                        "w-full transition-opacity duration-200 ease-out group-hover:opacity-80 " +
                        (isBest ? "bg-[#c2410c]" : "bg-stone-300")
                      }
                      style={{ height: `${(d.minutes / maxMinutes) * 100}%` }}
                    />
                  </div>
                );
              })}
            </div>
            <div className="mt-3 flex gap-3 sm:gap-5">
              {WEEK.map((d) => (
                <span
                  key={d.day}
                  className="flex-1 text-center text-[11px] font-medium uppercase tracking-[0.14em] text-stone-500"
                >
                  {d.day}
                </span>
              ))}
            </div>
          </div>

          <p className="mt-8 max-w-md text-sm leading-relaxed text-stone-500">
            Saturday carried the week. If today lands over 60 minutes,
            this becomes your most active week since March.
          </p>
        </section>
      </main>
    </div>
  );
}
