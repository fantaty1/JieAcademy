import request from './request'

export function getWeapons(params) {
  return request.get('/weapons/', { params })
}

export function getWeapon(id) {
  return request.get(`/weapons/${id}/`)
}

export function getWeaponCombos(weaponId, params) {
  return request.get(`/weapons/${weaponId}/combos/`, { params })
}
