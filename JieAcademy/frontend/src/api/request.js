import axios from 'axios'
import { getToken, removeToken } from '@/utils/auth'
import { ElMessage } from 'element-plus'

const request = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

request.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const { response } = error
    if (response) {
      if (response.status === 401) {
        removeToken()
        if (window.location.pathname !== '/login') {
          window.location.href = '/login'
        }
      } else if (response.status === 403) {
        ElMessage.error('没有权限')
      } else if (response.status >= 500) {
        ElMessage.error('服务器错误')
      }
    } else {
      ElMessage.error('网络连接失败')
    }
    return Promise.reject(error)
  }
)

export default request
