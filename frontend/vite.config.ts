import { resolve } from 'path';
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import legacy from '@vitejs/plugin-legacy';

const frontendPrefix = 'frontend';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    legacy({
      targets: ['defaults', 'not IE 11'],
    }),
  ],
  base: `/static/${frontendPrefix}/`,
  server: {
    host: true,
    port: 5173,
    origin: 'http://localhost:5173',
    watch: {
      usePolling: true // Required for WSL2
    },
  },
  build: {
    manifest: 'manifest.json',
    outDir: resolve(__dirname, `./dist/`),
    rollupOptions: {
      input: {
        main: './src/main.ts',
      },
      output: {
        // Remove hash from file name as it is added by Django on
        // collectstatic. Also place the files in the correct directory
        entryFileNames: 'js/[name].js',
        chunkFileNames: 'js/[name].js',
        assetFileNames: (assetInfo) => {
          let extType = 'misc';
          if (assetInfo.names) {
            extType = assetInfo?.names[0].split('.').at(1) ?? '';
          }
          if (/png|jpe?g|svg|gif|ico|webp|avif/i.test(extType)) {
            extType = 'img';
          } else if (/woff|woff2|eot|ttf|otf/.test(extType)) {
            extType = 'fonts';
          }
          return `${extType}/[name][extname]`;
        },
      },
    },
  },
  css: {
    devSourcemap: true,
  },
});
