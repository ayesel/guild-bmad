import './primitives.css';

export function Input({ label, hint, id, ...props }) {
  return (
    <label className="ui-field" htmlFor={id}>
      <span className="ui-field__label">{label}</span>
      <input className="ui-input" id={id} {...props} />
      {hint ? <span className="ui-field__hint">{hint}</span> : null}
    </label>
  );
}
