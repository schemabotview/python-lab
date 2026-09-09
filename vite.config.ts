import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { BASE_PATH } from './scripts/base.mjs'

// `base` is the deploy subpath for the production BUILD only: the app is served
// at graphl.in/python-lab/ as part of the GraphL catalog, so built asset URLs must
// be subpath-relative. Dev/serve stays at "/" so `npm run dev` is unaffected.
//
// Anything resolving a URL at runtime must use import.meta.env.BASE_URL rather
// than a leading-slash literal — see src/runtime/worker.ts and src/main.tsx.
export default defineConfig(({ command }) => ({
  base: command === 'build' ? BASE_PATH : '/',
  plugins: [react()],
}))
