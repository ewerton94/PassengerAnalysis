import { configure } from 'quasar/wrappers'
import { config as loadEnv } from 'dotenv'

loadEnv()

export default configure(function (/* ctx */) {
  return {
    eslint: {
      warnings: false,
      errors: false
    },

    boot: [
      'axios',
      'charts'
    ],

    css: [
      'app.scss'
    ],

    extras: [
      'roboto-font',
      'material-icons',
      'fontawesome-v6'
    ],

    build: {
      target: {
        browser: ['es2022', 'firefox115', 'chrome115', 'safari14'],
        node: 'node20'
      },
      vueRouterMode: 'hash',
      env: {
        GoogleMapsKey: process.env.GoogleMapsKey || ''
      },
      vitePlugins: []
    },

    devServer: {
      open: true,
      host: '127.0.0.1',
      port: 8080
    },

    framework: {
      config: {},
      plugins: [
        'Notify',
        'Loading',
        'Dialog'
      ]
    },

    animations: [],

    ssr: {
      pwa: false,
      prodPort: 3000,
      middlewares: [
        'render'
      ]
    },

    pwa: {
      workboxMode: 'GenerateSW'
    }
  }
})
