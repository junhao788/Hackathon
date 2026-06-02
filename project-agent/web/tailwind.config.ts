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
          DEFAULT: "#d9f99d", // Lime-200
          hover: "#bef264",   // Lime-300
          dark: "#1a2e05"
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
