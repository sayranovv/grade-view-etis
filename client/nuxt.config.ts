export default defineNuxtConfig({
  modules: [
    '@nuxt/ui',
    "nuxt-charts",
    '@pinia/nuxt',
  ],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000'
    }
  },
})