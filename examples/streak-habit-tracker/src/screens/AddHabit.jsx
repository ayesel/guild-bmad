import { ArrowLeft, CalendarCheck, Check, Clock, Sparkles } from 'lucide-react';
import { Badge, Button, Card, Input } from '../system/primitives/index.js';
import './AddHabit.css';

const scheduleOptions = ['Weekdays', 'Every day', 'Custom'];

export function AddHabit({ onBack, onCreate }) {
  return (
    <main className="add-shell">
      <header className="add-header">
        <Button variant="quiet" icon={ArrowLeft} onClick={onBack}>Back</Button>
        <div>
          <Badge tone="info" icon={Sparkles}>New routine</Badge>
          <h1>Add a habit that can survive real life.</h1>
          <p>Choose a specific cue, a realistic cadence, and a fallback window for days that shift.</p>
        </div>
      </header>

      <section className="add-layout">
        <Card className="habit-form">
          <Input id="habit-name" label="Habit name" placeholder="Pack tomorrow's lunch" />
          <Input id="habit-cue" label="Cue" placeholder="After dinner cleanup" hint="Use an event you already notice." />
          <Input id="habit-project" label="Project" placeholder="Family admin" />

          <fieldset className="schedule-field">
            <legend>Schedule</legend>
            <div className="schedule-options">
              {scheduleOptions.map((option) => (
                <label key={option} className="schedule-option">
                  <input type="radio" name="schedule" defaultChecked={option === 'Weekdays'} />
                  <span>{option}</span>
                </label>
              ))}
            </div>
          </fieldset>

          <div className="form-actions">
            <Button variant="secondary" onClick={onBack}>Cancel</Button>
            <Button icon={Check} onClick={onCreate}>Create habit</Button>
          </div>
        </Card>

        <aside className="preview-stack" aria-label="Habit setup preview">
          <Card tone="strong" className="preview-card">
            <CalendarCheck aria-hidden="true" />
            <h2>Weekday rhythm</h2>
            <p>Five small completions keep the streak visible without punishing weekend drift.</p>
          </Card>
          <Card tone="muted" className="preview-card">
            <Clock aria-hidden="true" />
            <h2>Fallback window</h2>
            <p>Late completions count when the cue moves, keeping recovery built into the system.</p>
          </Card>
        </aside>
      </section>
    </main>
  );
}
