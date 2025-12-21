import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // Cho phép truy cập từ domain ngrok/public
    allowedHosts: [
      '3195b999ad67.ngrok-free.app'
    ],
    // Nếu cần HMR qua ngrok, có thể bật host 0.0.0.0
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})

