import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      // On ajoute ici votre palette de couleurs TalAIt
      colors: {
        brand: {
          50: '#F0F7FF',  // Fond très clair
          100: '#E0F0FE',
          500: '#4A90E2', // Votre Bleu principal
          600: '#357ABD', // Hover
          900: '#1E3A8A', // Texte foncé
        },
      },
    },
  },
  plugins: [],
};

export default config;