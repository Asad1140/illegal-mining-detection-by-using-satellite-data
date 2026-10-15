/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        gov: {
          dark: '#0a192f',
          navy: '#0f172a',
          slate: '#1e293b',
          card: '#ffffff',
          border: '#e2e8f0',
          accent: '#2563eb',
          safe: '#16a34a',
          warning: '#eab308',
          danger: '#dc2626',
          purple: '#9333ea'
        }
      }
    },
  },
  plugins: [],
}
