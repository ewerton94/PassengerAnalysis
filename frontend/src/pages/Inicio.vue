<template>
  <div class="q-pa-lg">
    <transition
      appear
      enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut"
    >
      <q-option-group
        v-model="linhasEscolhidas"
        :options="linhas"
        name="nome"
        color="green"
        type="checkbox"
      />
    </transition>
    <q-btn
      label="Enviar"
      v-show="!visible"
      flat
      class="bg-primary text-white"
      align="right"
      @click="enviarLinhas"
    />
    <q-inner-loading :showing="visible">
      <q-spinner-oval size="50px" color="primary" />
    </q-inner-loading>
  </div>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useCoreStore } from 'stores/core'

export default {
  data () {
    return {
      linhasEscolhidas: [],
      visible: true
    }
  },
  created () {
    this.start()
  },
  computed: {
    ...mapState(useCoreStore, ['linhas'])
  },
  methods: {
    ...mapActions(useCoreStore, ['listarLinhas', 'CLEAN_EXTRA_FILTRO']),
    async start () {
      await this.listarLinhas()
      this.CLEAN_EXTRA_FILTRO()
      this.visible = false
    },
    enviarLinhas () {
      this.visible = true
      const linhas = this.linhasEscolhidas.join(',')
      this.$router.push(`/dashboard/?linhas=${linhas}`)
    }
  }
}
</script>
