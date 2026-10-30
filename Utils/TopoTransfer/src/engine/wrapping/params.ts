import type { MaskMode } from '../constraints/mask';

/** Artist-facing wrapping parameters. See docs/ALGORITHM.md for the mapping to the energy. */
export interface WrapParams {
  /** Scales the surface-fit term relative to stiffness, landmarks and protection. 0–2. */
  fitStrength: number;
  /** 0 = flexible (fits fine detail), 1 = stiff. Sets the final stiffness λ_end = 10^(−4+3s). */
  smoothness: number;
  /** Number of stiffness-annealing levels (coarse → fine). */
  levels: number;
  /** Maximum non-rigid ICP iterations per level. */
  iterationsPerLevel: number;
  /** Correspondence rejection radius as a fraction of the reference bounding-box diagonal. */
  maxCorrespondenceDistance: number;
  /** 0 = point-to-point, 1 = point-to-plane (lets the surface slide along the reference). */
  normalAlignment: number;
  /** Reject correspondences whose normals differ by more than this angle (degrees). */
  normalThresholdDeg: number;
  /** Treat reference normals as unoriented (for scans with inconsistent normals). */
  twoSidedNormals: boolean;
  /** Global multiplier on landmark weights. */
  landmarkInfluence: number;
  /** Strength of protected regions, 0–1. */
  regionInfluence: number;
  /** How the painted mask is interpreted. */
  maskMode: MaskMode;
  /** Also pull the base towards reference points it does not yet cover. */
  bidirectional: boolean;
  /** Reject correspondences landing on reference (or base) open boundaries. */
  rejectBoundary: boolean;
  /**
   * Allow bounded local uniform scaling in the stiffness term (as-similar-as-
   * possible). Lets proportions change without fighting the stiffness;
   * `maxLocalScale` bounds the scale factor to [1/max, max].
   */
  allowLocalScaling: boolean;
  maxLocalScale: number;
  /** Keep coincident but unconnected base vertices (UV / hard-edge splits) together. */
  seamLock: boolean;
  /** Relative residual tolerance of the linear solver. */
  solverTolerance: number;
  /** Maximum conjugate-gradient iterations per solve. */
  maxSolverIterations: number;
}

export const DEFAULT_WRAP_PARAMS: WrapParams = {
  fitStrength: 1,
  smoothness: 0.25,
  levels: 4,
  iterationsPerLevel: 6,
  maxCorrespondenceDistance: 0.1,
  normalAlignment: 0.3,
  normalThresholdDeg: 60,
  twoSidedNormals: false,
  landmarkInfluence: 1,
  regionInfluence: 1,
  maskMode: 'protect',
  bidirectional: true,
  rejectBoundary: true,
  allowLocalScaling: true,
  maxLocalScale: 1.5,
  seamLock: true,
  solverTolerance: 1e-5,
  maxSolverIterations: 300,
};

export const PARAM_LIMITS: Record<keyof Pick<WrapParams,
  'fitStrength' | 'smoothness' | 'levels' | 'iterationsPerLevel' | 'maxCorrespondenceDistance' | 'normalAlignment' | 'normalThresholdDeg' | 'landmarkInfluence' | 'regionInfluence'>, [number, number]> = {
  fitStrength: [0, 2],
  smoothness: [0, 1],
  levels: [1, 8],
  iterationsPerLevel: [1, 50],
  maxCorrespondenceDistance: [0.001, 1],
  normalAlignment: [0, 0.95],
  normalThresholdDeg: [5, 180],
  landmarkInfluence: [0, 10],
  regionInfluence: [0, 1],
};

/** Clamp/validate parameters; throws on non-finite input. */
export function sanitizeParams(p: Partial<WrapParams>): WrapParams {
  const out: WrapParams = { ...DEFAULT_WRAP_PARAMS, ...p };
  for (const [key, [lo, hi]] of Object.entries(PARAM_LIMITS)) {
    const k = key as keyof typeof PARAM_LIMITS;
    const v = out[k];
    if (typeof v !== 'number' || !Number.isFinite(v)) throw new Error(`Parameter ${k} must be a finite number.`);
    out[k] = Math.min(hi, Math.max(lo, v));
  }
  out.levels = Math.round(out.levels);
  out.iterationsPerLevel = Math.round(out.iterationsPerLevel);
  if (!(out.maxLocalScale >= 1) || !Number.isFinite(out.maxLocalScale)) out.maxLocalScale = DEFAULT_WRAP_PARAMS.maxLocalScale;
  out.maxLocalScale = Math.min(out.maxLocalScale, 4);
  if (!(out.solverTolerance > 0)) out.solverTolerance = DEFAULT_WRAP_PARAMS.solverTolerance;
  if (!(out.maxSolverIterations >= 1)) out.maxSolverIterations = DEFAULT_WRAP_PARAMS.maxSolverIterations;
  return out;
}

export type Quality = 'fast' | 'balanced' | 'high';

/**
 * Solver-effort presets. "high" is the best setting measured on the human
 * body ground truth (docs/HUMANS.md); "balanced" is the default.
 */
export const QUALITY_PRESETS: Record<Quality, Pick<WrapParams, 'levels' | 'iterationsPerLevel'>> = {
  fast: { levels: 3, iterationsPerLevel: 4 },
  balanced: { levels: 4, iterationsPerLevel: 6 },
  high: { levels: 6, iterationsPerLevel: 10 },
};

export function qualityOf(p: Pick<WrapParams, 'levels' | 'iterationsPerLevel'>): Quality | 'custom' {
  for (const [k, v] of Object.entries(QUALITY_PRESETS)) if (v.levels === p.levels && v.iterationsPerLevel === p.iterationsPerLevel) return k as Quality;
  return 'custom';
}

/** Stiffness schedule λ_k for each level, high → low. */
export function stiffnessSchedule(p: WrapParams): number[] {
  const lambdaEnd = Math.pow(10, -4 + 3 * p.smoothness);
  const lambdaStart = Math.max(lambdaEnd, 0.1);
  if (p.levels <= 1) return [lambdaEnd];
  const out: number[] = [];
  for (let k = 0; k < p.levels; k++) {
    const t = k / (p.levels - 1);
    out.push(lambdaStart * Math.pow(lambdaEnd / lambdaStart, t));
  }
  return out;
}
