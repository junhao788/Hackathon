import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0a0a0a",
        surface: "#171717",
        border: "#262626",
        accent: {
          DEFAULT: "#3b82f6", // blue-500
          hover: "#60a5fa",   // blue-400
          dark: "#1e3a8a"     // blue-900
        },
        text: {
          primary: "#ffffff",
          secondary: "#a1a1aa", // zinc-400
          tertiary: "#52525b"   // zinc-600
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      }
    },
  },
  plugins: [],
};
export default config;
