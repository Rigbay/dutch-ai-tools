/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        ink: '#111a24',
        muted: '#536474',
        linen: '#f1f5fa',
        paper: '#ffffff',
        leaf: '#2357df',
        clay: '#d45645',
        brass: '#e0992e',
        accent: '#7c3aed'
      },
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        serif: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif']
      },
      boxShadow: {
        soft: '0 20px 50px rgba(17, 26, 36, 0.10)'
      }
    }
  },
  plugins: []
};
