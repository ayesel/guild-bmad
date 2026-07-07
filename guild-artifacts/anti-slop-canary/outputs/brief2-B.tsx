import React from "react";
import { Footprints, Flame, Timer, Zap, ArrowUpRight, ArrowDownRight } from "lucide-react";

/**
 * Stride — Home Dashboard
 *
 * Visual direction: warm editorial. Serif display type over a paper-cream
 * ground, ink-green primary with a clay accent. Cards are flat, bordered,
 * and hairline-divided — no glass, no gradients, no uniform shadow soup.
 */

// ---------------------------------------------------------------------------
// Data
// ---------------------------------------------------------------------------

type Stat = {
  id: string;
  label: string;
  value: string;
  unit: string;
  delta: number; // percent vs. last week
  detail: string;
  icon: React.ComponentType<{ size?: number; strokeWidth?: number; className?: string }>;
};

const STATS: Stat[] = [
  {
    id: "steps",
    label: "Steps",
    value: "9,482",
    unit: "of 10,000",
    delta: 12,
    detail: "94% of daily goal",
    icon: Footprints,
  },
  {
    id: "calories",
    label: "Calories",
    value: "612",
    unit: "kcal burned",
    delta: 8,
    detail: "Above weekly average",
    icon: Flame,
  },
  {
    id: "active",
    label: "Active minutes",
    value: "47",
    unit: "of 60 min",
    delta: -6,
    detail: "13 min to close the ring",
    icon: Timer,
  },
  {
    id: "streak",
    label: "Streak",
    value: "16",
    unit: "days",
    delta: 0,
    detail: "Best: 23 days",
    icon: Zap,
  },
];

type Day = {
  label: string;
  minutes: number;
  isToday?: boolean;
};

const WEEK: Day[] = [
  { label: "Mon", minutes: 52 },
  { label: "Tue", minutes: 38 },
  { label: "Wed", minutes: 64 },
  { label: "Thu", minutes: 21 },
  { label: "Fri", minutes: 58 },
  { label: "Sat", minutes: 74 },
  { label: "Sun", minutes: 47, isToday: true },
];

const WEEKLY_GOAL_MINUTES = 60;
const MAX_MINUTES = Math.max(...WEEK.map((d) => d.minutes), WEEKLY_GOAL_MINUTES);
const TOTAL_MINUTES = WEEK.reduce((sum, d) => sum + d.minutes, 0);

// ---------------------------------------------------------------------------
// Pieces
// ---------------------------------------------------------------------------

function DeltaTag({ delta }: { delta: number }) {
  if (delta === 0) {
    return (
      <span className="text-xs font-medium tracking-wide text-stone-500">
        steady
      </span>
    );
  }
  const up = delta > 0;
  return (
    <span
      className={`inline-flex items-center gap-0.5 text-xs font-medium tabular-nums ${
        up ? "text-emerald-800" : "text-orange-800"
      }`}
    >
      {up ? (
        <ArrowUpRight size={13} strokeWidth={2} />
      ) : (
        <ArrowDownRight size={13} strokeWidth={2} />
      )}
      {Math.abs(delta)}%
    </span>
  );
}

function StatCard({ stat }: { stat: Stat }) {
  const Icon = stat.icon;
  return (
    <article className="flex flex-col justify-between rounded-md border border-stone-300 bg-white px-5 py-4">
      <div className="flex items-baseline justify-between">
        <h3 className="text-xs font-semibold uppercase tracking-[0.14em] text-stone-500">
          {stat.label}
        </h3>
        <DeltaTag delta={stat.delta} />
      </div>

      <div className="mt-5 flex items-end gap-3">
        <p className="font-serif text-4xl leading-none text-stone-900 tabular-nums">
          {stat.value}
        </p>
        <p className="pb-0.5 text-sm text-stone-500">{stat.unit}</p>
      </div>

      <div className="mt-4 flex items-center justify-between border-t border-stone-200 pt-3">
        <p className="text-xs text-stone-500">{stat.detail}</p>
        <Icon size={16} strokeWidth={1.75} className="text-stone-400" />
      </div>
    </article>
  );
}

function WeekBar({ day }: { day: Day }) {
  const heightPct = Math.round((day.minutes / MAX_MINUTES) * 100);
  const metGoal = day.minutes >= WEEKLY_GOAL_MINUTES;

  return (
    <div className="flex flex-1 flex-col items-center gap-2">
      <span className="text-xs text-stone-500 tabular-nums">{day.minutes}</span>
      <div className="flex h-40 w-full items-end justify-center">
        <div
          className={`w-full max-w-[2.75rem] rounded-t-sm transition-[height] duration-500 ease-out ${
            day.isToday
              ? "bg-orange-700"
              : metGoal
              ? "bg-emerald-900"
              : "bg-emerald-900/30"
          }`}
          style={{ height: `${heightPct}%` }}
          role="img"
          aria-label={`${day.label}: ${day.minutes} active minutes${
            metGoal ? ", goal met" : ""
          }`}
        />
      </div>
      <span
        className={`text-xs ${
          day.isToday ? "font-semibold text-orange-800" : "text-stone-500"
        }`}
      >
        {day.label}
      </span>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Dashboard
// ---------------------------------------------------------------------------

export default function Dashboard() {
  const today = new Date();
  const dateLabel = today.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
  });
  const hour = today.getHours();
  const greeting =
    hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";

  const goalDays = WEEK.filter((d) => d.minutes >= WEEKLY_GOAL_MINUTES).length;

  return (
    <div className="min-h-screen bg-[#f6f2ea] font-sans text-stone-900 antialiased">
      <main className="mx-auto max-w-5xl px-6 py-12 md:px-10">
        {/* Header */}
        <header className="flex flex-wrap items-end justify-between gap-4 border-b-2 border-stone-900 pb-6">
          <div>
            <h1 className="font-serif text-4xl leading-tight tracking-tight md:text-5xl">
              {greeting}, Maya.
            </h1>
            <p className="mt-2 text-sm text-stone-600">
              {dateLabel} · Day 16 of your streak
            </p>
          </div>
          <p className="text-sm text-stone-600">
            <span className="font-serif text-2xl text-stone-900 tabular-nums">
              {TOTAL_MINUTES}
            </span>{" "}
            active minutes this week
          </p>
        </header>

        {/* Stats */}
        <section aria-labelledby="today-heading" className="mt-10">
          <h2
            id="today-heading"
            className="text-xs font-semibold uppercase tracking-[0.14em] text-stone-500"
          >
            Today
          </h2>
          <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {STATS.map((stat) => (
              <StatCard key={stat.id} stat={stat} />
            ))}
          </div>
        </section>

        {/* Weekly activity */}
        <section aria-labelledby="week-heading" className="mt-12">
          <div className="flex flex-wrap items-baseline justify-between gap-2">
            <h2
              id="week-heading"
              className="text-xs font-semibold uppercase tracking-[0.14em] text-stone-500"
            >
              This week
            </h2>
            <p className="text-sm text-stone-600">
              Goal met on{" "}
              <span className="font-medium text-stone-900">
                {goalDays} of 7 days
              </span>
            </p>
          </div>

          <div className="mt-4 rounded-md border border-stone-300 bg-white px-6 pb-5 pt-6">
            <div className="relative">
              {/* Goal line */}
              <div
                className="pointer-events-none absolute inset-x-0 border-t border-dashed border-stone-400"
                style={{
                  top: `calc(1.25rem + ${
                    (1 - WEEKLY_GOAL_MINUTES / MAX_MINUTES) * 10
                  }rem)`,
                }}
                aria-hidden="true"
              >
                <span className="absolute -top-2.5 right-0 bg-white pl-2 text-[11px] text-stone-500">
                  {WEEKLY_GOAL_MINUTES} min goal
                </span>
              </div>

              <div className="flex items-end gap-3 md:gap-5">
                {WEEK.map((day) => (
                  <WeekBar key={day.label} day={day} />
                ))}
              </div>
            </div>

            <div className="mt-5 flex flex-wrap items-center gap-x-6 gap-y-2 border-t border-stone-200 pt-4 text-xs text-stone-600">
              <span className="inline-flex items-center gap-2">
                <span className="h-2.5 w-2.5 rounded-[2px] bg-emerald-900" />
                Goal met
              </span>
              <span className="inline-flex items-center gap-2">
                <span className="h-2.5 w-2.5 rounded-[2px] bg-emerald-900/30" />
                Under goal
              </span>
              <span className="inline-flex items-center gap-2">
                <span className="h-2.5 w-2.5 rounded-[2px] bg-orange-700" />
                Today
              </span>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
