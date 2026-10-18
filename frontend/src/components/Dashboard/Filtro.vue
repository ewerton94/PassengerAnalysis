<template>
  <div class="q-ma-md">
    <q-expansion-item expand-separator icon="filter_alt" label="Filtro">
      <div class="row justify-between q-my-md">
        <div class="col-12 col-md-3 q-pa-sm">
          <div class="row">
            <q-btn-dropdown color="primary" class="col-12 col-md-12">
              <template v-slot:label>
                <div class="row items-center no-wrap">
                  <q-icon left class="float-left" name="calendar_today" />
                  <q-separator />
                  <div class="text-center">
                    Dias de análise<br /><small>Filtro por data</small>
                  </div>
                </div>
              </template>
              <div class="col-12 q-ma-md">
                <q-input
                  class="col-12 q-mt-md"
                  filled
                  label="Data inicial"
                  v-model="filtrarDataInicial"
                  mask="date"
                >
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy ref="qDateProxyInicio" transition-show="scale" transition-hide="scale">
                        <q-date
                          v-model="filtrarDataInicial"
                          @update:model-value="() => $refs.qDateProxyInicio.hide()"
                        />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
                <q-separator />
                <q-input
                  class="col-12 q-mt-md"
                  filled
                  label="Data final"
                  v-model="filtrarDataFinal"
                  mask="date"
                >
                  <template v-slot:append>
                    <q-icon name="event" class="cursor-pointer">
                      <q-popup-proxy ref="qDateProxyFim" transition-show="scale" transition-hide="scale">
                        <q-date
                          v-model="filtrarDataFinal"
                          @update:model-value="() => $refs.qDateProxyFim.hide()"
                        />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </div>
            </q-btn-dropdown>
          </div>
        </div>

        <div class="col-12 col-md-3 q-pa-sm">
          <div class="row">
            <q-btn-dropdown color="primary" class="col-12 col-md-12">
              <template v-slot:label>
                <div class="row items-center no-wrap">
                  <q-icon left name="calendar_today" />
                  <div class="text-center">
                    Dia da semana<br /><small>Filtro por dia</small>
                  </div>
                </div>
              </template>
              <div class="col-12 q-ma-md">
                <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="1" label="Domingo" />
                <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="2" label="Segunda-Feira" />
                <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="3" label="Terça-Feira" />
                <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="4" label="Quarta-Feira" />
                <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="5" label="Quinta-Feira" />
                <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="6" label="Sexta-Feira" />
                <q-checkbox class="col-12" v-model="filtrarDiasDaSemana" :val="7" label="Sábado" />
              </div>
            </q-btn-dropdown>
          </div>
        </div>

        <div class="col-12 col-md-3 q-pa-sm">
          <div class="row">
            <q-btn-dropdown color="primary" class="col-12 col-md-12">
              <template v-slot:label>
                <div class="row items-center no-wrap">
                  <q-icon left name="timer" />
                  <div class="text-center">
                    Faixa Horária de Embarque<br /><small>Filtro por hora</small>
                  </div>
                </div>
              </template>
              <div class="col-12 q-ma-md">
                <q-input
                  class="col-12 q-mt-md"
                  filled
                  label="Hora inicial"
                  v-model="filtrarHoraInicialEmbarque"
                  mask="time"
                >
                  <template v-slot:append>
                    <q-icon name="timer" class="cursor-pointer">
                      <q-popup-proxy ref="qTimeProxyInicio" transition-show="scale" transition-hide="scale">
                        <q-time
                          v-model="filtrarHoraInicialEmbarque"
                          @update:model-value="() => $refs.qTimeProxyInicio.hide()"
                        />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
                <q-separator />
                <q-input
                  class="col-12 q-mt-md"
                  filled
                  label="Hora final"
                  v-model="filtrarHoraFinalEmbarque"
                  mask="time"
                >
                  <template v-slot:append>
                    <q-icon name="timer" class="cursor-pointer">
                      <q-popup-proxy ref="qTimeProxyFim" transition-show="scale" transition-hide="scale">
                        <q-time
                          v-model="filtrarHoraFinalEmbarque"
                          @update:model-value="() => $refs.qTimeProxyFim.hide()"
                        />
                      </q-popup-proxy>
                    </q-icon>
                  </template>
                </q-input>
              </div>
            </q-btn-dropdown>
          </div>
        </div>

        <div class="col-12 col-md-3 q-pa-sm">
          <div class="row">
            <q-btn-dropdown color="primary" class="col-12 col-md-12">
              <template v-slot:label>
                <div class="row items-center no-wrap">
                  <q-icon left name="alt_route" />
                  <div class="text-center">
                    Sentido de viagem<br /><small>Filtro por sentido</small>
                  </div>
                </div>
              </template>
              <div class="col-12 q-ma-md">
                <q-select
                  class="col-12"
                  outlined
                  v-model="filtrarSentido"
                  :options="['IDA', 'VOLTA', 'AMBOS']"
                >
                  <template v-slot:prepend>
                    <q-icon name="alt_route" />
                  </template>
                </q-select>
              </div>
            </q-btn-dropdown>
          </div>
        </div>
      </div>

      <div class="row justify-end">
        <q-btn
          label="Filtrar"
          align="right"
          flat
          color="white"
          class="bg-primary"
          @click="filtrarDados"
          :disable="!detailComplete"
        />
      </div>
    </q-expansion-item>
  </div>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useCoreStore } from 'stores/core'

export default {
  name: 'FiltroDashboard',
  data () {
    return {
      filtrarDataInicial: null,
      filtrarDataFinal: null,
      filtrarDiasDaSemana: [],
      filtrarHoraInicialEmbarque: null,
      filtrarHoraFinalEmbarque: null,
      filtrarSentido: 'AMBOS'
    }
  },
  computed: {
    ...mapState(useCoreStore, ['extraFiltro', 'detailComplete'])
  },
  methods: {
    ...mapActions(useCoreStore, [
      'ADD_NEW_EXTRA_FILTRO',
      'ICREMENT_GERALKEY',
      'SET_ENDED',
      'detalharLinhas'
    ]),
    async filtrarDados () {
      await this.SET_ENDED(false)
      if (this.filtrarDataInicial && this.filtrarDataFinal) {
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'data_inicial',
          newExtraFiltroValue: this.filtrarDataInicial.replaceAll('/', '-')
        })
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'data_final',
          newExtraFiltroValue: this.filtrarDataFinal.replaceAll('/', '-')
        })
      }
      if (this.filtrarDiasDaSemana.length) {
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'dias_da_semana',
          newExtraFiltroValue: this.filtrarDiasDaSemana.join(',')
        })
      }
      if (this.filtrarHoraInicialEmbarque && this.filtrarHoraFinalEmbarque) {
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'embarque_inicial',
          newExtraFiltroValue: this.filtrarHoraInicialEmbarque
        })
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'embarque_final',
          newExtraFiltroValue: this.filtrarHoraFinalEmbarque
        })
      }
      if (this.filtrarSentido) {
        await this.ADD_NEW_EXTRA_FILTRO({
          newExtraFiltroKey: 'sentido',
          newExtraFiltroValue: this.filtrarSentido
        })
      }

      this.ICREMENT_GERALKEY()
      await this.detalharLinhas(this.extraFiltro)
    }
  }
}
</script>
