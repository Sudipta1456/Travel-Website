/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx}", // include all JS/TS/JSX/TSX files from pages
    "./components/**/*.{js,ts,jsx,tsx}", // include all files from the components directory
    "./app/**/*.{js,ts,jsx,tsx}", // for Next.js app directory structure
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require("@tailwindcss/forms"), // example plugin for forms
    require("@tailwindcss/typography"), // example plugin for typography
  ],
};
