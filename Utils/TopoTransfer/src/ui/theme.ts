import * as THREE from 'three';
import type { LandmarkGroup } from '../engine/landmarks/landmarks';

export const GROUP_COLORS: Record<LandmarkGroup, string> = {
  face: '#f2c14e',
  eyes: '#5ec8ff',
  nose: '#ff8a5b',
  mouth: '#e868b0',
  ears: '#8bd17c',
  body: '#b48cff',
  other: '#c9ced6',
};

/** Guide pairs: each pair has its own colour, the same on both meshes (red with red, blue with blue…). */
export const PAIR_COLORS = [
  '#ff4d4d', '#3d8bff', '#3fd16b', '#ffd23f', '#d65cff', '#2fe0e0', '#ff9a2e', '#ff6fb5',
  '#9be15d', '#8c7bff', '#ffffff', '#c0a070',
];

export function pairColor(id: number): string {
  return PAIR_COLORS[(Math.max(1, id) - 1) % PAIR_COLORS.length];
}

const STOPS: [number, string][] = [
  [0, '#1d3b8f'],
  [0.25, '#2a8cc9'],
  [0.5, '#3fbf8f'],
  [0.75, '#e8c547'],
  [1, '#e5533d'],
];
const STOP_COLORS = STOPS.map(([t, c]) => [t, new THREE.Color(c)] as const);

/** Map t in [0,1] (clamped) to a perceptually ordered blue→green→yellow→red ramp. */
export function heatColor(t: number, out: THREE.Color): THREE.Color {
  const x = Math.min(1, Math.max(0, t));
  for (let i = 1; i < STOP_COLORS.length; i++) {
    const [t1, c1] = STOP_COLORS[i];
    if (x <= t1) {
      const [t0, c0] = STOP_COLORS[i - 1];
      return out.copy(c0).lerp(c1, (x - t0) / (t1 - t0));
    }
  }
  return out.copy(STOP_COLORS[STOP_COLORS.length - 1][1]);
}

export const HEAT_GRADIENT_CSS = `linear-gradient(90deg, ${STOPS.map(([t, c]) => `${c} ${t * 100}%`).join(', ')})`;
