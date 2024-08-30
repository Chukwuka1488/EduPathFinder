// tailwind.config.js
module.exports = {
  purge: ["./index.html", "./scripts/**/*.js"], // Add the paths to all of your template files
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      colors: {
        "custom-orange": "#F05023",
        "custom-green": "#356829",
        "custom-gray": "#5a5a5a",
        "custom-blue": "#00008b",
        "custom-light": "#AAB8C2",
      },
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
};
