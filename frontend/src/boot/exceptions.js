import { Loading, Notify } from 'quasar'

const handleError = async (err) => {
  Loading.hide()
  let message = 'Erro inesperado'
  if (err?.message === 'Network Error') {
    message = 'Sem internet / API indisponível'
  } else if (err?.response?.status === 500) {
    message = 'Erro no servidor'
  } else if (err?.response?.data) {
    const data = err.response.data
    if (typeof data === 'string') {
      message = data
    } else if (data.detail) {
      message = data.detail
    } else {
      const key = Object.keys(data)[0]
      const value = Object.values(data)[0]
      message = key + ': ' + value
    }
  }

  Notify.create({
    type: 'negative',
    message
  })
}

export {
  handleError
}
