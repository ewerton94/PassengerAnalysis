import { defineStore } from 'pinia'
import { HTTPClient } from 'boot/axios'
import { handleError } from 'boot/exceptions'
import { Notify } from 'quasar'

function serialize (obj) {
  const str = []
  for (const p in obj) {
    str.push(encodeURIComponent(p) + '=' + encodeURIComponent(obj[p]))
  }
  return str.join('&')
}

async function adaptObjectToList (list, idName, getLabelName) {
  list.forEach((el) => {
    el.value = el[idName]
    el.label = getLabelName(el)
  })
}

export const useCoreStore = defineStore('Core', {
  state: () => ({
    linhas: [],
    linha: {},
    graficos: {},
    geralKey: 0,
    extraFiltro: {},
    detailComplete: false
  }),

  actions: {
    async SET_LINHAS (payload) {
      await adaptObjectToList(payload, 'numero', (el) => (el.numero + ' - ' + el.nome))
      this.linhas = payload
    },
    SET_INFO_LINHAS (payload) {
      this.linha = payload
      this.detailComplete = true
    },
    SET_INFO_GRAFICO (payload) {
      this.graficos[payload.tipoGrafico] = payload.data
    },
    ICREMENT_GERALKEY () {
      this.geralKey = this.geralKey + 1
    },
    SET_ENDED (payload) {
      this.detailComplete = payload
    },
    SET_EXTRA_FILTRO (extraFiltro) {
      this.extraFiltro = extraFiltro
      this.ICREMENT_GERALKEY()
    },
    CLEAN_EXTRA_FILTRO () {
      this.extraFiltro = {}
    },
    ADD_NEW_EXTRA_FILTRO ({ newExtraFiltroKey, newExtraFiltroValue }) {
      this.extraFiltro[newExtraFiltroKey] = newExtraFiltroValue
      this.ICREMENT_GERALKEY()
    },
    ADD_EXTRA_FILTRO_INICIAL ({ newExtraFiltroKey, newExtraFiltroValue }) {
      this.extraFiltro[newExtraFiltroKey] = newExtraFiltroValue
    },

    listarLinhas () {
      return new Promise((resolve, reject) => {
        HTTPClient.get('core/linhas/')
          .then(async (suc) => {
            await this.SET_LINHAS(suc.data)
            resolve(suc.data)
          })
          .catch(async (err) => {
            await handleError(err)
            reject(err)
          })
      })
    },

    detalharLinhas (extraFiltro) {
      return new Promise((resolve, reject) => {
        HTTPClient.get(`core/linhas/detalhar/?${serialize(extraFiltro)}`)
          .then(async (suc) => {
            await this.SET_INFO_LINHAS(suc.data)
            resolve(suc.data)
          })
          .catch(async (err) => {
            await handleError(err)
            reject(err)
          })
      })
    },

    obterDadosGrafico (extraFiltro) {
      return new Promise((resolve, reject) => {
        HTTPClient.get(`core/linhas/grafico/?${serialize(extraFiltro)}`)
          .then(async (suc) => {
            await this.SET_INFO_GRAFICO({ data: suc.data, tipoGrafico: extraFiltro.tipo_grafico })
            resolve(suc.data)
          })
          .catch(async (err) => {
            await handleError(err)
            reject(err)
          })
      })
    },

    calcularDesembarque () {
      return new Promise((resolve, reject) => {
        HTTPClient.get('core/linhas/calcular_desembarque/')
          .then(async (suc) => {
            Notify.create({
              type: 'positive',
              message: 'Ok'
            })
            resolve(suc.data)
          })
          .catch(async (err) => {
            await handleError(err)
            reject(err)
          })
      })
    }
  }
})
