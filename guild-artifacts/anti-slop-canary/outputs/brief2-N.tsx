import React from "react";
import { Footprints, Flame, Timer, Zap, TrendingUp } from "lucide-react";

type Stat = {
  id: string;
  label: string;
  value: string;
  sub: string;
  icon: React.ComponentType<{ className?: string }>;
  iconBg: string;
  iconColor: string;
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
    sub: "Goal 10,000",
    icon: Footprints,
    iconBg: "bg-emerald-100",
    iconColor: "text-emerald-600",
  },
  {
    id: "calories",
    label: "Calories",
    value: "612",
    sub: "kcal burned",
    icon: Flame,
    iconBg: "bg-orange-100",
    iconColor: "text-orange-600",
  },
  {
    id: "active-minutes",
    label: "Active Minutes",
    value: "47",
    sub: "Goal 60 min",
    icon: Timer,
    iconBg: "bg-sky-100",
    iconColor: "text-sky-600",
  },
  {
    id: "streak",
    label: "Streak",
    value: "12 days",
    sub: "Personal best: 21",
    icon: Zap,
    iconBg: "bg-violet-100",
    iconColor: "text-violet-600",
  },
];

const WEEKLY_ACTIVITY: DayActivity[] = [
  { day: "Mon", minutes: 38 },
  { day: "Tue", minutes: 52 },
  { day: "Wed", minutes: 24 },
  { day: "Thu", minutes: 61 },
  { day: "Fri", minutes: 45 },
  { day: "Sat", minutes: 74 },
  { day: "Sun", minutes: 47 },
];

function formatDate(date: Date): string {
  return date.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric",
  });
}

function greetingForHour(hour: number): string {
  if (hour < 5) return "Still up";
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  return "Good evening";
}

function StatCard({ stat }: { stat: Stat }) {
  const Icon = stat.icon;
  return (
    <div className="flex items-start gap-4 rounded-xl border border-slate-200 bg-white p-5 shadow-sm">
      <div
        className={`flex h-10 w-10 shrink-0 items-center justify-center rounded-lg ${stat.iconBg}`}
      >
        <Icon className={`h-5 w-5 ${stat.iconColor}`} />
      </div>
      <div className="min-w-0">
        <p className="text-sm font-medium text-slate-500">{stat.label}</p>
        <p className="mt-1 text-2xl font-semibold tracking-tight text-slate-900">
          {stat.value}
        </p>
        <p className="mt-0.5 text-xs text-slate-400">{stat.sub}</p>
      </div>
    </div>
  );
}

function WeeklyActivityChart({ data }: { data: DayActivity[] }) {
  const max = Math.max(...data.map((d) => d.minutes), 1);
  const total = data.reduce((sum, d) => sum + d.minutes, 0);
  const todayIndex = data.length - 1;

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-base font-semibold text-slate-900">
            Weekly Activity
          </h2>
          <p className="mt-0.5 text-sm text-slate-500">
            {total} active minutes this week
          </p>
        </div>
        <div className="flex items-center gap-1.5 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
          <TrendingUp className="h-3.5 w-3.5" />
          On track
        </div>
      </div>

      <div className="flex h-48 items-end gap-3 sm:gap-4">
        {data.map((d, i) => {
          const isToday = i === todayIndex;
          const heightPct = Math.round((d.minutes / max) * 100);
          return (
            <div
              key={d.day}
              className="flex h-full flex-1 flex-col items-center justify-end gap-2"
            >
              <span className="text-xs font-medium text-slate-500">
                {d.minutes}
              </span>
              <div
                className={`w-full max-w-10 rounded-t-md ${
                  isToday ? "bg-emerald-500" : "bg-slate-200"
                }`}
                style={{ height: `${heightPct}%` }}
                role="img"
                aria-label={`${d.day}: ${d.minutes} active minutes`}
              />
              <span
                className={`text-xs ${
                  isToday
                    ? "font-semibold text-slate-900"
                    : "font-medium text-slate-400"
                }`}
              >
                {d.day}
              </span>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default function Dashboard() {
  const now = new Date();

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <main className="mx-auto max-w-5xl px-4 py-8 sm:px-6 sm:py-12">
        <header className="mb-8">
          <p className="text-sm font-medium text-emerald-600">Stride</p>
          <h1 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
            {greetingForHour(now.getHours())}, Alex
          </h1>
          <p className="mt-1 text-sm text-slate-500">{formatDate(now)}</p>
        </header>

        <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {STATS.map((stat) => (
            <StatCard key={stat.id} stat={stat} />
          ))}
        </div>

        <WeeklyActivityChart data={WEEKLY_ACTIVITY} />
      </main>
    </div>
  );
}
