require('dotenv').config();

export default {
  mode: 'spa',
  head: {
    titleTemplate: '%s - ' + process.env.npm_package_name,
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: process.env.npm_package_description || '' }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }
    ]
  },
  loading: { color: '#fff' },
  buildModules: [
    '@nuxtjs/vuetify',

  ],
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    '@nuxtjs/dotenv',
  ],

  // Axios config
  axios: {
    baseURL:  process.env.API_URL
  },

   // Auth Config
  auth: {
    redirect: {
      login: '/login', // User will be redirected to this path if login is required.
      logout: '/login', // User will be redirected to this path if after logout
      home: '/' // User will be redirect to this path after login.
    },
    strategies: {
      local: {
        endpoints: {
          login: { url: '/login', method: 'post', propertyName: 'token' },
          logout: { url: '/logout', method: 'post' },
          user: { url: '/user', method: 'get', propertyName: 'user' }
        },

        tokenRequired: true
      }
    }
  },

  router: {
    // middleware: ['auth']
  },

  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    preset: "vue-cli-plugin-vuetify-preset-rally/preset"
  },

  build: {
    transpile: ["vue-cli-plugin-vuetify-preset-rally"],
  }
}
