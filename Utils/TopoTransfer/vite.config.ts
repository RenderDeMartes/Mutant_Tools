import fs from 'node:fs';
import path from 'node:path';
import { defineConfig, type Plugin } from 'vitest/config';
import react from '@vitejs/plugin-react';

// The bundle strips the libraries' license comments, so the build writes their
// licenses next to it: THIRD_PARTY_LICENSES.txt, one entry per npm package that
// actually ended up in a chunk.
function thirdPartyLicenses(): Plugin {
  return {
    name: 'third-party-licenses',
    apply: 'build',
    generateBundle(_options, bundle) {
      const roots = new Map<string, string>();
      for (const chunk of Object.values(bundle)) {
        if (chunk.type !== 'chunk') continue;
        for (const id of Object.keys(chunk.modules)) {
          // virtual ids (commonjs proxies) start with \0 and may end in ?query
          const file = id.replace(/^\0/, '').split('?')[0].replace(/\\/g, '/');
          const m = file.match(/^(.*\/node_modules\/)((?:@[^/]+\/)?[^/]+)\//);
          if (m) roots.set(m[2], m[1] + m[2]);
        }
      }
      const entries = [...roots.keys()].sort().map((name) => {
        const dir = roots.get(name)!;
        const pkg = JSON.parse(fs.readFileSync(path.join(dir, 'package.json'), 'utf8'));
        const file = fs.readdirSync(dir).find((f) => /^(licen[cs]e|copying)(\.|$)/i.test(f));
        const text = file ? fs.readFileSync(path.join(dir, file), 'utf8').trim() : `License: ${pkg.license}`;
        return `${name} ${pkg.version} (${pkg.license})\n${'-'.repeat(60)}\n${text}\n`;
      });
      this.emitFile({
        type: 'asset',
        fileName: 'THIRD_PARTY_LICENSES.txt',
        source: `TopoTransfer bundles the following open-source packages.\n\n${entries.join('\n\n')}`,
      });
    },
  };
}

// `--mode maya` (npm run build:maya) writes the lean copy that Maya serves itself (app/):
// no sourcemaps, and public/ (example meshes) is not copied — the Maya bridge serves it
// from public/ directly, so the meshes are not stored twice.
export default defineConfig(({ mode }) => {
  const maya = mode === 'maya';
  return {
    // relative asset URLs: the app works from any path (dev server, static host, Maya bridge)
    base: './',
    plugins: [react(), thirdPartyLicenses()],
    worker: { format: 'es' },
    build: {
      target: 'es2022',
      sourcemap: !maya,
      outDir: maya ? 'app' : 'dist',
      emptyOutDir: true,
      copyPublicDir: !maya,
      chunkSizeWarningLimit: 700,
      rollupOptions: { output: { manualChunks: { three: ['three'] } } },
    },
    test: {
      include: ['tests/**/*.test.ts'],
      testTimeout: 120_000,
    },
  };
});
