/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "SFMono-Regular", "monospace"],
      },
      colors: {
        ink: "#080B10",
        slatepanel: "#111820",
        panel: "#161E27",
        borderline: "rgba(255,255,255,0.10)",
        aqua: "#2DD4BF",
        gold: "#F59E0B",
        steel: "#94A3B8",
        blue: "#60A5FA",
      },
      boxShadow: {
        panel: "0 22px 70px rgba(0,0,0,.38)",
        lift: "0 18px 45px rgba(45,212,191,.14)",
        innerPanel: "inset 0 1px 0 rgba(255,255,255,.08)",
      },
      keyframes: {
        blink: { "0%,45%": { opacity: "1" }, "46%,100%": { opacity: "0" } },
        float: { "0%,100%": { transform: "translateY(0)" }, "50%": { transform: "translateY(-16px)" } },
        orbit: { "0%": { transform: "rotate(0deg)" }, "100%": { transform: "rotate(360deg)" } },
        dash: { "0%": { strokeDashoffset: "220" }, "100%": { strokeDashoffset: "0" } },
      },
      animation: {
        blink: "blink 1s steps(1) infinite",
        float: "float 7s ease-in-out infinite",
        orbit: "orbit 14s linear infinite",
        dash: "dash 2.4s ease-in-out infinite alternate",
      },
    },
  },
  plugins: [],
};
