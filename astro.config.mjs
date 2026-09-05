// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

// https://astro.build/config
export default defineConfig({
  // Fully static output. There is no server runtime; the whole site is
  // pre-rendered to HTML at build time and can be hosted anywhere.
  output: "static",

  site: "https://www.winters-yonker.com",

  build: {
    // Emit /about/index.html rather than /about.html so URLs stay
    // extension-free on any static host.
    format: "directory",

    // The page's CSS is ~9 KB. Shipping it as a separate file cost 160ms of
    // render blocking on throttled 4G; inlining removes that request entirely.
    inlineStylesheets: "always",
  },

  vite: {
    plugins: [tailwindcss()],
  },
});
