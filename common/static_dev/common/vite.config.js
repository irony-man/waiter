import { fileURLToPath, URL } from "url";

// eslint-disable-next-line no-undef
import { resolve } from "path";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import {sentryVitePlugin} from "@sentry/vite-plugin";

// https://vitejs.dev/config/
export default defineConfig({
  mode: process.env.NODE_ENV === "production" ? "production" : "development",
  plugins: [
    vue(),
 ],
  base: "/static/common/",
  build: {
    manifest: true,
    ssrManifest: true,
    cssCodeSplit: true,
    sourcemap: process.env.NODE_ENV !== "production",
    rollupOptions: {
      input: {
        main: resolve("./src/main.js"),
        style: resolve("./src/styles/style.scss"),
      },
    },
    minify: false,
    outDir: resolve("../../static/common/"),
    emptyOutDir: true,
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
