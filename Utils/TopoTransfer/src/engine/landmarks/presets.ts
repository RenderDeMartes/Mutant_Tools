/**
 * Named landmark sets for human faces and bodies. Names ending in " L" / " R"
 * are left/right pairs (character's left = +X in a front-facing, Y-up mesh)
 * and can be mirrored across the symmetry plane.
 */

import type { LandmarkGroup } from './landmarks';

export interface PresetPoint {
  name: string;
  group: LandmarkGroup;
  /** short placement hint shown while placing */
  hint: string;
}

export type PresetKind = 'face' | 'body';

const pair = (name: string, group: LandmarkGroup, hint: string): PresetPoint[] => [
  { name: `${name} L`, group, hint: `${hint} (character's left)` },
  { name: `${name} R`, group, hint: `${hint} (character's right)` },
];

export const FACE_PRESET: PresetPoint[] = [
  { name: 'Glabella', group: 'face', hint: 'Between the eyebrows, most forward point' },
  { name: 'Nasion', group: 'nose', hint: 'Deepest point of the nose bridge' },
  { name: 'Nose tip', group: 'nose', hint: 'Most forward point of the nose (pronasale)' },
  { name: 'Subnasale', group: 'nose', hint: 'Where the nose septum meets the upper lip' },
  ...pair('Nose ala', 'nose', 'Outermost point of the nostril wing'),
  ...pair('Eye inner corner', 'eyes', 'Inner canthus'),
  ...pair('Eye outer corner', 'eyes', 'Outer canthus'),
  ...pair('Upper eyelid', 'eyes', 'Middle of the upper lid margin'),
  ...pair('Lower eyelid', 'eyes', 'Middle of the lower lid margin'),
  ...pair('Brow peak', 'face', 'Highest point of the eyebrow arch'),
  ...pair('Mouth corner', 'mouth', 'Lip commissure'),
  { name: 'Upper lip center', group: 'mouth', hint: 'Centre of the upper lip vermilion border' },
  { name: 'Lower lip center', group: 'mouth', hint: 'Centre of the lower lip vermilion border' },
  { name: 'Chin', group: 'face', hint: 'Most forward point of the chin (pogonion)' },
  { name: 'Chin bottom', group: 'face', hint: 'Lowest point of the chin (menton)' },
  ...pair('Jaw angle', 'face', 'Corner of the jaw (gonion)'),
  ...pair('Cheekbone', 'face', 'Most prominent point of the cheekbone'),
  ...pair('Ear top', 'ears', 'Highest point of the ear helix'),
  ...pair('Tragus', 'ears', 'Small flap in front of the ear canal'),
  ...pair('Earlobe', 'ears', 'Lowest point of the earlobe'),
];

export const BODY_PRESET: PresetPoint[] = [
  { name: 'Head top', group: 'body', hint: 'Highest point of the skull' },
  { name: 'Nose tip', group: 'nose', hint: 'Most forward point of the nose' },
  { name: 'Chin', group: 'face', hint: 'Most forward point of the chin' },
  { name: 'Neck front', group: 'body', hint: 'Suprasternal notch, top of the sternum' },
  { name: 'Neck back', group: 'body', hint: 'Most prominent neck vertebra (C7)' },
  ...pair('Shoulder', 'body', 'Top of the shoulder (acromion)'),
  ...pair('Nipple', 'body', 'Centre of the nipple'),
  { name: 'Navel', group: 'body', hint: 'Centre of the navel' },
  { name: 'Crotch', group: 'body', hint: 'Lowest point between the legs' },
  ...pair('Elbow', 'body', 'Tip of the elbow (olecranon)'),
  ...pair('Wrist', 'body', 'Back of the wrist, ulnar bump'),
  ...pair('Thumb tip', 'body', 'Tip of the thumb'),
  ...pair('Index fingertip', 'body', 'Tip of the index finger'),
  ...pair('Middle fingertip', 'body', 'Tip of the middle finger'),
  ...pair('Little fingertip', 'body', 'Tip of the little finger'),
  ...pair('Hip bone', 'body', 'Front hip bone (anterior superior iliac spine)'),
  ...pair('Knee', 'body', 'Centre of the kneecap'),
  ...pair('Ankle', 'body', 'Outer ankle bone (lateral malleolus)'),
  ...pair('Heel', 'body', 'Back of the heel'),
  ...pair('Big toe tip', 'body', 'Tip of the big toe'),
];

/**
 * MetaHuman mode: the head vertex of each face guide on the MetaHuman LOD0 head (the first mesh of
 * Meta Mutant's export, so the index is the OBJ vertex index). Every MetaHuman head shares this
 * topology, so the Base side of the guides can be placed for you. Found on Ada's head (eye lids
 * around the eyeball, the nose / lip / chin profile on the midline, the ears as what sticks out
 * sideways) and checked by eye.
 */
export const METAHUMAN_HEAD_VERTICES = 24049;
// no Brow peak: the brows do not help place the joints (the free Face set still has them)
export const METAHUMAN_FACE_VERTEX: Record<string, number> = {
  'Nose tip': 17088,
  'Nasion': 9854,
  'Glabella': 16130,
  'Subnasale': 12818,
  'Upper lip center': 2909,
  'Lower lip center': 2881,
  'Chin': 2971,
  'Chin bottom': 2977,
  'Eye inner corner L': 4076,
  'Eye outer corner L': 22252,
  'Upper eyelid L': 9699,
  'Lower eyelid L': 9305,
  'Nose ala L': 22337,
  'Mouth corner L': 21624,
  'Cheekbone L': 4910,
  'Ear top L': 4853,
  'Earlobe L': 8011,
  'Tragus L': 5299,
  'Jaw angle L': 23934,
  'Eye inner corner R': 13836,
  'Eye outer corner R': 19239,
  'Upper eyelid R': 19741,
  'Lower eyelid R': 15290,
  'Nose ala R': 700,
  'Mouth corner R': 18611,
  'Cheekbone R': 1839,
  'Ear top R': 1782,
  'Earlobe R': 13989,
  'Tragus R': 2228,
  'Jaw angle R': 20921,
};

export const PRESETS: Record<PresetKind, PresetPoint[]> = { face: FACE_PRESET, body: BODY_PRESET };

/** Name of the mirrored counterpart ("Ear top L" ↔ "Ear top R"), or null for centre-line points. */
export function mirrorName(name: string): string | null {
  if (name.endsWith(' L')) return name.slice(0, -2) + ' R';
  if (name.endsWith(' R')) return name.slice(0, -2) + ' L';
  return null;
}

export function presetHint(name: string): string | undefined {
  for (const p of [...FACE_PRESET, ...BODY_PRESET]) if (p.name === name) return p.hint;
  return undefined;
}
