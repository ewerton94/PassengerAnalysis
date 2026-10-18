<template>
  <q-card :key="key">
    <q-card-section>
      <div class="text-h6">{{ title }}</div>
      <div class="text-subtitle2">{{ subtitle }}</div>
    </q-card-section>

    <q-card-section class="q-pt-none q-pa-none q-ma-none">
      <div :ref="divId" :id="divId" />
    </q-card-section>
    <q-card-section v-show="!dadosObtidos" class="q-pt-none">
      <q-skeleton height="300px" square />
    </q-card-section>
  </q-card>
</template>

<script>
import Plotly from 'plotly.js-dist-min'
import { mapState, mapActions } from 'pinia'
import { useCoreStore } from 'stores/core'

export default {
  name: 'GraficoPlotly',
  props: [
    'tipoGrafico',
    'modeloGrafico',
    'title',
    'subtitle',
    'divId',
    'timeout'
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
      this.$nextTick(() => {
        const el = this.$refs[this.divId]
        if (!el || !this.graficos[this.tipoGrafico]) return
        let layout = { ...this.graficos[this.tipoGrafico].layout }
        if (this.$q.screen.lt.md) {
          layout.showlegend = false
          layout.margin = { l: 0, r: 0, b: 0, t: 0, pad: 4 }
          layout.yaxis = Object.assign({}, layout.yaxis, { fixedrange: true })
          layout.xaxis = Object.assign({}, layout.xaxis, { fixedrange: true })
        }
        Plotly.newPlot(el, this.graficos[this.tipoGrafico].data, layout, { responsive: true })
      })
    }
  }
}
</script>
