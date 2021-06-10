
const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'dashboard', component: () => import('pages/Dashboard.vue') },
      { path: '', component: () => import('pages/Inicio.vue') }
    ],
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/login',
    component: () => import('layouts/Login.vue'),
    meta: {
      guest: true
    },
    name: 'login'
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
