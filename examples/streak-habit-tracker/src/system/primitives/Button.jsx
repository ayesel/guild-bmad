import './primitives.css';

export function Button({ children, variant = 'primary', size = 'md', icon: Icon, ...props }) {
  return (
    <button className={`ui-button ui-button--${variant} ui-button--${size}`} {...props}>
      {Icon ? <Icon aria-hidden="true" className="ui-button__icon" /> : null}
      <span>{children}</span>
    </button>
  );
}
