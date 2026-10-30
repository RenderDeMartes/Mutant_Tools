/**
 * Launch parameters (`?base=…&reference=…&return=…`) used by the Maya window
 * in maya/tt_bridge.py: only loopback URLs are accepted, fetches refuse
 * redirects and send no credentials, results are POSTed as a simple request.
 */
import { describe, expect, it, vi } from 'vitest';
import { fetchLaunchFile, fileNameFromUrl, hasLaunchParams, isLoopbackUrl, parseLaunchParams, postResult, stripLaunchParams } from '../src/state/launch';

const TOKEN = 'abc123';
const base = `http://127.0.0.1:51234/${TOKEN}/files/mh_head_lod0.obj`;
const ref = `http://127.0.0.1:51234/${TOKEN}/files/custom_head.obj`;
const ret = `http://127.0.0.1:51234/${TOKEN}/result`;

function fakeFetch(body: string, status = 200) {
  return vi.fn(async (_url: string | URL | Request, _init?: RequestInit) => new Response(body, { status }));
}

describe('isLoopbackUrl', () => {
  it.each(['http://127.0.0.1:5000/x', 'http://localhost:5000/x', 'https://localhost/x', 'http://[::1]:8080/x', 'http://LOCALHOST:1/x'])('accepts %s', (u) => {
    expect(isLoopbackUrl(u)).toBe(true);
  });

  it.each([
    'http://example.com/x',
    'http://127.0.0.1.example.com/x',
    'http://localhost.example.com/x',
    'http://192.168.1.10/x',
    'http://0.0.0.0/x',
    'http://user:pw@127.0.0.1/x',
    'http://evil.com@127.0.0.1.nip.io/x',
    'file:///C:/secret.obj',
    'ftp://127.0.0.1/x',
    'javascript:alert(1)',
    'data:text/plain,v 0 0 0',
    '//127.0.0.1/x',
    '/relative/path.obj',
    'not a url',
  ])('rejects %s', (u) => {
    expect(isLoopbackUrl(u)).toBe(false);
  });
});

describe('parseLaunchParams', () => {
  it('reads encoded base, reference and return URLs', () => {
    const q = `?base=${encodeURIComponent(base)}&reference=${encodeURIComponent(ref)}&return=${encodeURIComponent(ret)}`;
    const p = parseLaunchParams(q);
    expect(p).toEqual({ base, reference: ref, returnUrl: ret, errors: [] });
    expect(hasLaunchParams(p)).toBe(true);
  });

  it('is empty without parameters', () => {
    const p = parseLaunchParams('?foo=1');
    expect(p).toEqual({ base: null, reference: null, returnUrl: null, errors: [] });
    expect(hasLaunchParams(p)).toBe(false);
  });

  it('rejects non-loopback URLs per parameter and keeps the valid ones', () => {
    const q = `?base=${encodeURIComponent('https://example.com/a.obj')}&reference=${encodeURIComponent(ref)}&return=${encodeURIComponent('http://10.0.0.2/result')}`;
    const p = parseLaunchParams(q);
    expect(p.base).toBeNull();
    expect(p.reference).toBe(ref);
    expect(p.returnUrl).toBeNull();
    expect(p.errors).toHaveLength(2);
    expect(p.errors[0]).toMatch(/"base"/);
    expect(p.errors[1]).toMatch(/"return"/);
    expect(hasLaunchParams(p)).toBe(true);
  });
});

describe('URL helpers', () => {
  it('strips only the launch parameters', () => {
    const href = `http://localhost:5173/app/?x=1&base=${encodeURIComponent(base)}&return=${encodeURIComponent(ret)}#h`;
    expect(stripLaunchParams(href)).toBe('http://localhost:5173/app/?x=1#h');
  });

  it('derives file names from the last path segment', () => {
    expect(fileNameFromUrl(base, 'base.obj')).toBe('mh_head_lod0.obj');
    expect(fileNameFromUrl('http://127.0.0.1:1/t/files/my%20head.obj?x=1', 'f.obj')).toBe('my head.obj');
    expect(fileNameFromUrl('http://127.0.0.1:1/t/files/a%2Fb.obj', 'f.obj')).toBe('a_b.obj');
    expect(fileNameFromUrl('http://127.0.0.1:1/', 'f.obj')).toBe('f.obj');
  });
});

describe('fetchLaunchFile', () => {
  it('fetches without credentials or redirects and names the file from the URL', async () => {
    const f = fakeFetch('v 0 0 0\n');
    const res = await fetchLaunchFile(base, 'base.obj', f as unknown as typeof fetch);
    expect(res.name).toBe('mh_head_lod0.obj');
    expect(new TextDecoder().decode(res.buffer)).toBe('v 0 0 0\n');
    expect(f).toHaveBeenCalledOnce();
    const init = f.mock.calls[0][1]!;
    expect(init.credentials).toBe('omit');
    expect(init.redirect).toBe('error');
  });

  it('refuses non-loopback URLs without fetching', async () => {
    const f = fakeFetch('');
    await expect(fetchLaunchFile('http://example.com/a.obj', 'a.obj', f as unknown as typeof fetch)).rejects.toThrow(/loopback/);
    expect(f).not.toHaveBeenCalled();
  });

  it('reports HTTP errors', async () => {
    await expect(fetchLaunchFile(base, 'a.obj', fakeFetch('no', 403) as unknown as typeof fetch)).rejects.toThrow(/403/);
  });
});

describe('postResult', () => {
  it('POSTs the data as a CORS simple request and returns the JSON message', async () => {
    const f = fakeFetch(JSON.stringify({ ok: true, message: 'saved mh_head_lod0_wrapped.obj' }));
    const data = new TextEncoder().encode('# Exported by TopoTransfer\nv 1 2 3\n').buffer as ArrayBuffer;
    expect(await postResult(ret, data, f as unknown as typeof fetch)).toBe('saved mh_head_lod0_wrapped.obj');
    const [url, init] = f.mock.calls[0];
    expect(url).toBe(ret);
    expect(init!.method).toBe('POST');
    expect(init!.credentials).toBe('omit');
    expect(init!.redirect).toBe('error');
    // only CORS-safelisted headers, so the browser sends no preflight
    expect(Object.keys(init!.headers as Record<string, string>)).toEqual(['Content-Type']);
    expect((init!.headers as Record<string, string>)['Content-Type']).toBe('text/plain');
    expect(await (init!.body as Blob).text()).toBe('# Exported by TopoTransfer\nv 1 2 3\n');
  });

  it('throws the receiver message on errors', async () => {
    const f = fakeFetch(JSON.stringify({ ok: false, message: 'expected 12 vertices, got 3' }), 422);
    await expect(postResult(ret, new ArrayBuffer(0), f as unknown as typeof fetch)).rejects.toThrow('expected 12 vertices, got 3');
  });

  it('refuses non-loopback return URLs without sending', async () => {
    const f = fakeFetch('');
    await expect(postResult('https://example.com/upload', new ArrayBuffer(0), f as unknown as typeof fetch)).rejects.toThrow(/loopback/);
    expect(f).not.toHaveBeenCalled();
  });
});
