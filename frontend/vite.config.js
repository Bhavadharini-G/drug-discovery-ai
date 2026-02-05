import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],

  root: ".", // frontend is the root for Vite

  build: {
    outDir: "dist",
    emptyOutDir: true,
    chunkSizeWarningLimit: 2000,
  },

  resolve: {
    alias: {
      "@": "/src",
    },
  },

  css: {
    devSourcemap: true,
  },
});
