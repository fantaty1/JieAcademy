import request from './request'

// 获取所有贡献列表 (可以按 target_id, target_type, category 过滤)
export function getContributions(params) {
  return request.get('/contributions/', { params })
}

// 发布新的连招或感悟
export function createContribution(data) {
  return request.post('/contributions/', data)
}

// 获取单条详情 (不常用)
export function getContribution(id) {
  return request.get(`/contributions/${id}/`)
}

// 删除贡献
export function deleteContribution(id) {
  return request.delete(`/contributions/${id}/`)
}

// 修改贡献
export function updateContribution(id, data) {
  return request.put(`/contributions/${id}/`, data)
}
