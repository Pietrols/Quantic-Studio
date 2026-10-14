// Node 25 and later define a global localStorage of their own (undefined unless
// --localstorage-file is given), which shadows jsdom's Web Storage. Bind
// jsdom's storage so the tests see what a browser would, on any Node version.
const dom = (globalThis as { jsdom?: { window: Window } }).jsdom;
if (dom) {
  for (const name of ["localStorage", "sessionStorage"] as const) {
    Object.defineProperty(globalThis, name, {
      value: dom.window[name],
      configurable: true,
      writable: true,
    });
  }
}
