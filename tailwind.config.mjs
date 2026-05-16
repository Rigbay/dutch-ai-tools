/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        ink: '#1a1a2e',
        muted: '#5c6378',
        linen: '#f0f4ff',
        paper: '#fafbff',
        leaf: '#2563eb',
        clay: '#e05a3e',
        brass: '#e0992e',
        accent: '#7c3aed'
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['Georgia', 'ui-serif', 'serif']
      },
      boxShadow: {
        soft: '0 20px 50px rgba(26, 26, 46, 0.08)'
      }
    }
  },
  plugins: []
};
