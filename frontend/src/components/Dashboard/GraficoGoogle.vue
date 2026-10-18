<template>
  <q-card :key="key">
    <q-card-section>
      <div class="text-h6">{{ title }}</div>
      <div class="text-subtitle2">{{ subtitle }}</div>
    </q-card-section>

    <q-card-section v-if="graficos[tipoGrafico] && dadosObtidos" class="q-pt-none">
      <GChart
        type="Sankey"
        :data="graficos[tipoGrafico].data"
        :options="graficos[tipoGrafico].layout"
        :settings="{ packages: ['sankey'] }"
      />
    </q-card-section>
    <q-card-section v-if="!dadosObtidos" class="q-pt-none">
      <q-skeleton height="300px" square />
    </q-card-section>
  </q-card>
</template>

<script>
import { GChart } from 'vue-google-charts'
import { mapState, mapActions } from 'pinia'
import { useCoreStore } from 'stores/core'

export default {
  name: 'GraficoGoogle',
  components: { GChart },
  props: [
    'tipoGrafico',
    'modeloGrafico',
    'title',
    'subtitle'
  ],
  data () {
    return {
      dadosObtidos: false,
      key: 0
    }
  },
  computed: {
    ...mapState(useCoreStore, ['graficos', 'extraFiltro'])
  },
  created () {
    this.start()
  },
  methods: {
    ...mapActions(useCoreStore, ['obterDadosGrafico']),
    async start () {
      let extraFiltro = JSON.parse(JSON.stringify(this.extraFiltro))
      extraFiltro.tipo_grafico = this.tipoGrafico
      await this.obterDadosGrafico(extraFiltro)
      this.dadosObtidos = true
      this.key = this.key + 1
    }
  }
}
</script>
