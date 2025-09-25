import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    host: true,
  },
  preview: {
    host: true,
    allowedHosts: ['easyapi-crud-demo.onrender.com'],
  },
})


