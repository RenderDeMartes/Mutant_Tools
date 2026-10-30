import { ReactNode, useEffect, useState } from 'react';

export function Section(props: { title: string; children: ReactNode; right?: ReactNode; defaultOpen?: boolean; hint?: string }) {
  const [open, setOpen] = useState(props.defaultOpen ?? true);
  return (
    <section className="section">
      <header className="section-head" onClick={() => setOpen(!open)} title={props.hint}>
        <span className={`chev ${open ? 'open' : ''}`}>▸</span>
        <span className="section-title">{props.title}</span>
        <span className="section-right" onClick={(e) => e.stopPropagation()}>
          {props.right}
        </span>
      </header>
      {open && <div className="section-body">{props.children}</div>}
    </section>
  );
}

export function Slider(props: {
  label: string;
  value: number;
  min: number;
  max: number;
  step?: number;
  onChange: (v: number) => void;
  format?: (v: number) => string;
  hint?: string;
  disabled?: boolean;
  log?: boolean;
}) {
  const { min, max, log } = props;
  const toSlider = (v: number) => (log ? Math.log10(v) : v);
  const fromSlider = (v: number) => (log ? Math.pow(10, v) : v);
  const step = props.step ?? (max - min) / 100;
  return (
    <label className={`slider ${props.disabled ? 'disabled' : ''}`} title={props.hint}>
      <span className="slider-label">{props.label}</span>
      <input
        type="range"
        min={toSlider(min)}
        max={toSlider(max)}
        step={log ? (toSlider(max) - toSlider(min)) / 200 : step}
        value={toSlider(props.value)}
        disabled={props.disabled}
        onChange={(e) => props.onChange(fromSlider(parseFloat(e.target.value)))}
      />
      <NumberInput value={props.value} min={min} max={max} step={step} onChange={props.onChange} format={props.format} disabled={props.disabled} />
    </label>
  );
}

export function NumberInput(props: {
  value: number;
  onChange: (v: number) => void;
  min?: number;
  max?: number;
  step?: number;
  format?: (v: number) => string;
  disabled?: boolean;
  className?: string;
}) {
  const fmt = props.format ?? ((v: number) => (Math.abs(v) >= 100 ? v.toFixed(1) : Math.abs(v) >= 1 ? v.toFixed(2) : v.toFixed(3)));
  const [text, setText] = useState(fmt(props.value));
  const [focused, setFocused] = useState(false);
  useEffect(() => {
    if (!focused) setText(fmt(props.value));
  }, [props.value, focused]); // eslint-disable-line react-hooks/exhaustive-deps
  const commit = () => {
    const v = parseFloat(text);
    if (Number.isFinite(v)) {
      const c = Math.min(props.max ?? Infinity, Math.max(props.min ?? -Infinity, v));
      props.onChange(c);
      setText(fmt(c));
    } else setText(fmt(props.value));
  };
  return (
    <input
      className={`num ${props.className ?? ''}`}
      type="text"
      inputMode="decimal"
      value={text}
      disabled={props.disabled}
      onFocus={() => setFocused(true)}
      onBlur={() => {
        setFocused(false);
        commit();
      }}
      onChange={(e) => setText(e.target.value)}
      onKeyDown={(e) => {
        if (e.key === 'Enter') (e.target as HTMLInputElement).blur();
        if (e.key === 'Escape') {
          setText(fmt(props.value));
          (e.target as HTMLInputElement).blur();
        }
        e.stopPropagation();
      }}
    />
  );
}

export function Toggle(props: { label: string; checked: boolean; onChange: (v: boolean) => void; hint?: string; disabled?: boolean }) {
  return (
    <label className={`toggle ${props.disabled ? 'disabled' : ''}`} title={props.hint}>
      <input type="checkbox" checked={props.checked} disabled={props.disabled} onChange={(e) => props.onChange(e.target.checked)} />
      <span className="toggle-box" />
      <span>{props.label}</span>
    </label>
  );
}

export function Segmented<T extends string>(props: { value: T; options: { value: T; label: string; hint?: string }[]; onChange: (v: T) => void; disabled?: boolean }) {
  return (
    <div className="segmented">
      {props.options.map((o) => (
        <button
          key={o.value}
          className={o.value === props.value ? 'active' : ''}
          title={o.hint}
          disabled={props.disabled}
          onClick={() => props.onChange(o.value)}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

export function Kbd(props: { children: ReactNode }) {
  return <kbd className="kbd">{props.children}</kbd>;
}
