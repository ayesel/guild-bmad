import './primitives.css';

export function Badge({ children, tone = 'neutral', icon: Icon }) {
  return (
    <span className={`ui-badge ui-badge--${tone}`}>
      {Icon ? <Icon aria-hidden="true" className="ui-badge__icon" /> : null}
      {children}
    </span>
  );
}
