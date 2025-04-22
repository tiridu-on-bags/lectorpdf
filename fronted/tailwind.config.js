/** @type {import('tailwindcss').Config} */
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        'background': '#faf4ea', // Beige
        'primary-text': '#333333', // Dark Gray/Almost Black
        'secondary-text': '#747C71', // Green
        'structure-alt': '#8a7769', // Brown
        'accent': '#4A6B8A', // Deep Blue (chosen accent)
        'accent-hover': '#3B5670', // Darker blue for hover
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'], // Example: Using Inter font
      },
    },
  },
  plugins: [
    forms,
    typography,
  ],
} 