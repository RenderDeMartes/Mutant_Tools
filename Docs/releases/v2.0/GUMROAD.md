<!-- Gumroad post / customer update. Gumroad's editor is rich text: paste the text, then bold the headings. -->

# Mutant Tools 2.0 is out

Mutant Tools 2.0 rebuilds the core rigging blocks to play back faster, gives animators more
control, and makes builds easier to fix when something goes wrong. Your 1.6 rigs keep building
as they did, and you can move each block to its new version when you're ready.

**What's new**

- **Faster biped and animal blocks.** Spine, Limb, Head, Hand, Foot, QuadLimb and QuadSpine are
  rebuilt on matrix nodes, with up to about 2x faster playback.
- **More controls for animators.** Spine squash & stretch with tweakers, bendy limbs that curve
  into a true arc, a neck you can curve from the top, and IK fingers that don't flip.
- **Wings v002.** Add or remove feathers live, curve them, and spread or fold whole wings with
  two controls.
- **A local face that matches the game mouth.** Lips v003, Jaw v002 and StickyLips v002 bring the
  MouthGames features to the layered face.
- **Squash v002.** Squash any geo with a lattice of FK rows and edge controls.
- **A Build Log you can read.** Every block is listed with its build time, and the one that failed
  opens with a likely cause.
- **Safer rebuilds.** Skins survive missing joints and load about 3x faster.
- **A new AutoRigger panel and help everywhere.** Block settings show as cards, an eye button
  compares block versions, and you can right click any button and pick Learn more.

**How to update:** download the new zip from your Gumroad library, or use the update check in the
Mutant-Tools menu. Then drag `easy_install.py` into Maya.

Full release notes, with every block change:
https://github.com/RenderDeMartes/Mutant_Tools/releases/tag/v2.0
