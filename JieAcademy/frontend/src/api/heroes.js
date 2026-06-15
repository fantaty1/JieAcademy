import request from './request'

export function getHeroes(params) {
  return request.get('/heroes/', { params })
}

export function getHero(id) {
  return request.get(`/heroes/${id}/`)
}

export function getHeroCombos(heroId, params) {
  return request.get(`/heroes/${heroId}/combos/`, { params })
}

export function getHeroMatchups(heroId, params) {
  return request.get(`/heroes/${heroId}/matchups/`, { params })
}
