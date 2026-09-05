/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        radar: {
          950: '#07090E',
          900: '#0B0F17',
          850: '#101622',
          800: '#151E2E',
          700: '#1E293B',
          600: '#334155',
          border: '#1E293B',
          accent: '#38BDF8',
          danger: '#F43F5E',
          warning: '#F59E0B',
          success: '#10B981',
        },
      },
      fontFamily: {
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [],
};