/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        dark: {
          900: "#0a0a0f",
          800: "#12121a",
          700: "#1a1a25",
          600: "#242432",
          500: "#2e2e40",
        },
        accent: {
          cyan: "#00ffc8",
          pink: "#ff0064",
          purple: "#a855f7",
          blue: "#3b82f6",
        },
      },
    },
  },
  plugins: [],
};
