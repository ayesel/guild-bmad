import { ArrowUpRight, CalendarDays, Flame, Plus, Target, TimerReset } from 'lucide-react';
import { Badge, Button, Card } from '../system/primitives/index.js';
import './Dashboard.css';

const habits = [
  {
    name: 'Morning walk',
    project: 'Health',
    streak: '18 days',
    next: 'before school drop-off',
    progress: [true, true, true, true, true, false, true]
  },
  {
    name: 'Budget check',
    project: 'Home admin',
    streak: '6 days',
    next: 'after dinner',
    progress: [true, true, false, true, true, true, false]
  },
  {
    name: 'Read with Nora',
    project: 'Family',
    streak: '11 days',
    next: 'bedtime',
    progress: [true, true, true, true, false, true, true]
  }
];

const week = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];

export function Dashboard({ onAddHabit }) {
  return (
    <main className="dashboard-shell">
      <header className="dashboard-header">
        <div>
          <Badge tone="success" icon={Flame}>Current streaks</Badge>
          <h1>Keep the week moving.</h1>
          <p>Track compact routines across family, health, and admin without turning habits into another project.</p>
        </div>
        <Button icon={Plus} size="lg" onClick={onAddHabit}>Add habit</Button>
      </header>

      <section className="dashboard-grid" aria-label="Habit overview">
        <Card tone="strong" className="metric-card metric-card--hero">
          <span className="metric-card__label">Active streak</span>
          <strong>18</strong>
          <span>days walking before the day gets loud</span>
        </Card>
        <Card className="metric-card">
          <CalendarDays aria-hidden="true" />
          <span className="metric-card__label">This week</span>
          <strong>82%</strong>
          <span>completion across shared routines</span>
        </Card>
        <Card className="metric-card">
          <Target aria-hidden="true" />
          <span className="metric-card__label">Focus area</span>
          <strong>Family</strong>
          <span>highest recovery after missed days</span>
        </Card>
      </section>

      <section className="habit-layout">
        <div className="habit-list" aria-label="Tracked habits">
          {habits.map((habit) => (
            <Card key={habit.name} className="habit-card">
              <div className="habit-card__topline">
                <div>
                  <Badge tone="info">{habit.project}</Badge>
                  <h2>{habit.name}</h2>
                </div>
                <Button variant="quiet" size="sm" icon={ArrowUpRight}>Open</Button>
              </div>
              <div className="habit-card__meta">
                <span><Flame aria-hidden="true" />{habit.streak}</span>
                <span><TimerReset aria-hidden="true" />{habit.next}</span>
              </div>
              <div className="habit-week" aria-label={`${habit.name} weekly completion`}>
                {habit.progress.map((done, index) => (
                  <span className={done ? 'habit-day habit-day--done' : 'habit-day'} key={`${habit.name}-${week[index]}-${index}`}>
                    {week[index]}
                  </span>
                ))}
              </div>
            </Card>
          ))}
        </div>

        <Card tone="muted" className="coach-panel">
          <Badge tone="warning">Guild moment</Badge>
          <h2>Design nudges stay useful and quiet.</h2>
          <p>The screen uses dense rows, restrained color, and short motion so busy parents can scan recovery opportunities in seconds.</p>
          <Button variant="secondary" icon={CalendarDays}>Plan tomorrow</Button>
        </Card>
      </section>
    </main>
  );
}
