<template>
  <q-layout view="hHh lpR fFf">
    <q-page-container>
      <q-page class="flex flex-center bg-grey-2">
        <q-card style="width: 100%; max-width: 400px">
          <q-card-section>
            <div class="text-h6">Análises de Passageiros</div>
            <div class="text-subtitle2 text-grey-7">Entrar</div>
          </q-card-section>

          <q-card-section>
            <q-form @submit.prevent="login" class="q-gutter-md">
              <q-input
                v-model="username"
                label="Usuário"
                filled
                autocomplete="username"
                :disable="loading"
              />
              <q-input
                v-model="password"
                label="Senha"
                type="password"
                filled
                autocomplete="current-password"
                :disable="loading"
              />
              <q-btn
                type="submit"
                color="primary"
                label="Entrar"
                class="full-width"
                :loading="loading"
              />
            </q-form>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import { Loading, Notify } from 'quasar'
import { HTTPClient, keyToken } from 'boot/axios'

export default {
  name: 'LoginLayout',
  data () {
    return {
      username: '',
      password: '',
      loading: false
    }
  },
  methods: {
    async login () {
      if (!this.username || !this.password) {
        Notify.create({ type: 'warning', message: 'Informe usuário e senha' })
        return
      }

      this.loading = true
      Loading.show()
      try {
        const { data } = await HTTPClient.post('entrar/', {
          username: this.username,
          password: this.password
        })

        localStorage.setItem(keyToken + '-token', data.token)
        localStorage.setItem(keyToken, JSON.stringify(data.user || {}))
        HTTPClient.defaults.headers.common.Authorization = 'Token ' + data.token

        const nextUrl = this.$route.query.nextUrl || '/'
        this.$router.push(nextUrl)
      } catch (err) {
        const message = err?.response?.data?.detail || 'Falha no login'
        Notify.create({ type: 'negative', message })
      } finally {
        this.loading = false
        Loading.hide()
      }
    }
  }
}
</script>
