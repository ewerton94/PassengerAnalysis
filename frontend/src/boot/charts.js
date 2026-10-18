import { defineBoot } from '#q-app/wrappers'
import VueApexCharts from 'vue3-apexcharts'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret, faBus, faRoute, faUser, faFilter, faMapSigns, faCalculator } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUserSecret, faBus, faRoute, faUser, faFilter, faMapSigns, faCalculator)

export default defineBoot(({ app }) => {
  app.use(VueApexCharts)
  app.component('apexchart', VueApexCharts)
  app.component('font-awesome-icon', FontAwesomeIcon)
})
