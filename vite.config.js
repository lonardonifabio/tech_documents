import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { copyFileSync, mkdirSync, existsSync } from 'fs'
import { resolve } from 'path'

export default defineConfig({
  plugins: [
    react(),
    {
      name: 'copy-data',
      writeBundle() {
        // Ensure dist/data directory exists
        const distDataDir = resolve(__dirname, 'dist/data')
        if (!existsSync(distDataDir)) {
          mkdirSync(distDataDir, { recursive: true })
        }
        
        // Copy documents.json to dist/data
        const srcFile = resolve(__dirname, 'data/documents.json')
        const destFile = resolve(__dirname, 'dist/data/documents.json')
        
        if (existsSync(srcFile)) {
          copyFileSync(srcFile, destFile)
          console.log('✓ Copied documents.json to dist/data/')
        } else {
          console.warn('⚠ data/documents.json not found, creating empty array')
          // Create empty documents.json if it doesn't exist
          const fs = require('fs')
          fs.writeFileSync(destFile, '[]')
        }
      }
    }
  ],
  base: '/tech_documents/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
