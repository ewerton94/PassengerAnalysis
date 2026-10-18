import { defineBoot } from '#q-app/wrappers'
import axios from 'axios'
import { settings } from 'src/config/constants'

const apiLink = settings.apiLink
const version = settings.version
const compile = settings.compile
const keyToken = 'user_' + version + compile

const HTTPClient = axios.create({
  baseURL: apiLink
})

HTTPClient.defaults.withCredentials = true
HTTPClient.defaults.xsrfCookieName = 'csrftoken'
HTTPClient.defaults.xsrfHeaderName = 'X-CSRFToken'

const token = localStorage.getItem(keyToken + '-token')
if (token) {
  HTTPClient.defaults.headers.common.Authorization = 'Token ' + token
}

export default defineBoot(({ app }) => {
  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = HTTPClient
})

export { HTTPClient, keyToken }
