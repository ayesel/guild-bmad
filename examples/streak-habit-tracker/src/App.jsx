import { useState } from 'react';
import { Dashboard } from './screens/Dashboard.jsx';
import { AddHabit } from './screens/AddHabit.jsx';

export function App() {
  const [screen, setScreen] = useState('dashboard');

  return screen === 'dashboard' ? (
    <Dashboard onAddHabit={() => setScreen('add')} />
  ) : (
    <AddHabit onBack={() => setScreen('dashboard')} onCreate={() => setScreen('dashboard')} />
  );
}
