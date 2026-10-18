import { defineRouter } from '#q-app/wrappers'
import {
  createRouter,
  createMemoryHistory,
  createWebHistory,
  createWebHashHistory
} from 'vue-router'
import routes from './routes'
import { settings } from 'src/config/constants'

const version = settings.version
const compile = settings.compile
const keyToken = 'user_' + version + compile

export default defineRouter(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  Router.beforeEach((to, from, next) => {
    const hasToken = localStorage.getItem(keyToken + '-token') !== null

    if (to.matched.some(record => record.meta.requiresAuth)) {
      if (!hasToken) {
        next({ path: '/login', query: { nextUrl: to.fullPath } })
      } else {
        next()
      }
    } else if (to.matched.some(record => record.meta.guest)) {
      if (!hasToken) {
        next()
      } else {
        next({ path: '/' })
      }
    } else {
      next()
    }
  })

  return Router
})
