import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    outDir: 'static/build',
    emptyOutDir: true,
    rollupOptions: {
      input: 'frontend/main.js',
      output: {
        entryFileNames: 'iiol.js',
        assetFileNames: 'iiol[extname]',
      },
    },
  },
  test: {
    environment: 'node',
  },
});
