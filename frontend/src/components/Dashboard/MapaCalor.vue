<template>
  <q-card :key="key">
    <q-card-section>
      <div class="text-h6">{{ title }}</div>
      <div class="text-subtitle2">{{ subtitle }}</div>
    </q-card-section>

    <q-card-section v-if="graficos[tipoGrafico] && dadosObtidos" class="q-pt-none">
      <HeatMap
        :points="graficos[tipoGrafico].data"
        :lat="graficos[tipoGrafico].lat"
        :lng="graficos[tipoGrafico].lng"
        :initial-zoom="11"
        width="100%"
        :height="350"
      />
    </q-card-section>
    <q-card-section v-else-if="dadosObtidos && !hasMapsKey" class="q-pt-none text-grey-7">
      Defina GoogleMapsKey no arquivo .env para exibir o mapa de calor.
    </q-card-section>
    <q-card-section v-if="!dadosObtidos" class="q-pt-none">
      <q-skeleton height="300px" square />
    </q-card-section>
  </q-card>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useCoreStore } from 'stores/core'
import HeatMap from './HeatMap.vue'

export default {
  name: 'MapaCalor',
  components: { HeatMap },
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
    ...mapState(useCoreStore, ['graficos', 'extraFiltro']),
    hasMapsKey () {
      const key = (process.env.GoogleMapsKey || '').replaceAll('"', '').replaceAll("'", '')
      return Boolean(key)
    }
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
