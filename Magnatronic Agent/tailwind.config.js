/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./magnatronic/dashboard/**/*.{js,jsx}",
    "./magnatronic/templates/**/*.html"
  ],
  theme: {
    extend: {
      colors: {
        'electric-blue': '#3BE0F0',
        'vibrant-green': '#10B981',
        'golden-yellow': '#FFD700',
        'primary-bg': '#000000',
        'secondary-bg': '#111111',
      },
      fontFamily: {
        'mono': ['Fira Code', 'monospace'],
        'sans': ['Inter', 'system-ui', '-apple-system', 'sans-serif']
      }
    }
  },
  plugins: [
    require('@tailwindcss/forms')
  ]
}