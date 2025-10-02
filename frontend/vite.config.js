import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  // Base path for production deployment
  base: '/',
  
  // Build configuration
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'esbuild',
    target: 'es2015'
  },
  
  // Server configuration for development
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false
      }
    }
  },
  
  // Preview configuration
  preview: {
    port: 5173,
    host: true
  }
})
