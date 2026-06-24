import './primitives.css';

export function Card({ children, tone = 'default', className = '', ...props }) {
  return (
    <section className={`ui-card ui-card--${tone} ${className}`.trim()} {...props}>
      {children}
    </section>
  );
}
