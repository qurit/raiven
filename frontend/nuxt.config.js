require('dotenv').config()

export default {
  mode: 'spa',
  server: {
    host: process.env.NUXT_HOST || 'localhost',
    port: process.env.NUXT_PORT || 3000
  },
  head: {
    titleTemplate: 'Raiven',
    title: process.env.npm_package_name || '',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Quicksand&display=swap'
      }
    ]
  },
  loading: { color: '#B15DFF' },
  buildModules: ['@nuxtjs/vuetify'],
  modules: [
    '@nuxtjs/axios',
    '@nuxtjs/auth',
    '@nuxtjs/dotenv',
    'nuxt-socket-io'
  ],
  io: {
    sockets: [
      {
        url: 'http://localhost:5000'
      }
    ]
  },

  plugins: [
    '~/plugins/GlobalComponents',
    '~/plugins/toaster',
    '~/plugins/validation'
  ],

  // Axios config
  axios: {
    baseURL: process.env.API_URL || 'http://localhost:5000'
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
          login: {
            url: '/auth/token',
            method: 'post',
            propertyName: 'access_token'
          },
          user: { url: '/user/me', method: 'get', propertyName: '' }
        },

        tokenRequired: true
      }
    }
  },

  router: {
    middleware: ['auth']
  },

  vuetify: {
    customVariables: ['~/assets/variables.scss', '~/assets/overides.sass'],
    treeShake: true,
    theme: {
      options: { customProperties: true },
      dark: true,
      themes: {
        dark: {
          primary: '#fdbb16',
          secondary: '#771c46',
          accent: '#771c46',
          tertiary: '#FF6859',
          quaternary: '#FFCF44',
          quinary: '#B15DFF',
          senary: '#72DEFF',
          error: '#FF5252',
          info: '#2196F3',
          success: '#4CAF50',
          warning: '#FFC107',
          confirm: '#8BC34',
          cancel: '#F44336'
        }
      }
    }
  }
}
