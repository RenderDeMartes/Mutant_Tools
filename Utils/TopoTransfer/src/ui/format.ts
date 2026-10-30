import { get, Units } from '../state/store';

const TO_MM: Record<Exclude<Units, 'none'>, number> = { m: 1000, cm: 10, mm: 1 };

/** Format a length in scene units; shown in millimetres when the scene units are known. */
export function fmtLen(v: number, units: Units = get().units): string {
  if (!Number.isFinite(v)) return '—';
  if (units === 'none') return v === 0 ? '0' : v.toPrecision(3);
  const mm = v * TO_MM[units];
  return `${mm >= 100 ? mm.toFixed(0) : mm >= 10 ? mm.toFixed(1) : mm.toFixed(2)} mm`;
}
