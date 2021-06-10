<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          Análises de Passageiros
        </q-toolbar-title>

        <q-btn round flat>
            <q-avatar size="26px">

            </q-avatar>
            <q-tooltip>Account</q-tooltip>
            <q-menu transition-show="jump-down" transition-hide="jump-up">
              <q-list style="min-width: 100px">
                <q-item clickable>
                  <q-item-section @click="logout">Sair</q-item-section>
                </q-item>
              </q-list>
            </q-menu>
          </q-btn>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
      content-class="bg-grey-1"
    >
      <q-list>
        <q-item-label
          header
          class="text-grey-8"
        >
          Menu
        </q-item-label>
        <q-list>
        <q-item clickable v-close-popup to="/">
          <q-item-section avatar>
          <q-icon color="primary" name="dashboard" />
        </q-item-section>
          <q-item-section>
            <q-item-label>Dashboard</q-item-label>
          </q-item-section>
        </q-item>
        <!--

        <q-item clickable v-close-popup @click="calcularDesembarque">
          <q-item-section avatar>
          <q-icon color="primary" name="fas fa-calculator" />
        </q-item-section>
          <q-item-section>
            <q-item-label>Calcular Desembarques</q-item-label>
          </q-item-section>
        </q-item>-->

      </q-list>

      </q-list>
    </q-drawer>

    <q-page-container >
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { mapActions } from 'vuex'
import { Loading } from 'quasar'
import { settings } from '../config/constants'
import { HTTPClient } from 'boot/axios'
// const apiLink = settings.apiLink
const version = settings.version
// const appName = settings.appName
const compile = settings.compile
const keyToken = 'user_' + version + compile
export default {
  name: 'MainLayout',
  methods: {
    ...mapActions('Core', ['calcularDesembarque']),
    logout () {
      Loading.show()
      localStorage.removeItem(keyToken + '-token')
      localStorage.removeItem(keyToken)
      this.user = { username: '' }
      localStorage.setItem(keyToken + '-user_meta', '{}')
      this.$router.push({ name: 'login' })
      Loading.hide()
    },
    obterUsuarioLogado () {
      HTTPClient.get('obtem_usuario_logado/')
        .then(async response => {
          await response.data
          console.log(response.data)
          localStorage.setItem(
            keyToken + '-user_meta',
            JSON.stringify(response.data)
          )
          this.usuario = response.data
        })
        .catch(async err => {
          await err
          this.usuario = JSON.parse(localStorage.getItem(keyToken + '-user_meta'))
        })
    }
  },

  data () {
    return {
      leftDrawerOpen: false
    }
  }
}
</script>
