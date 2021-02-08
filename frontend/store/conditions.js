import { generic_get, generic_post } from '~/api'

export const state = () => ({
  conditions: []
})

export const mutations = {
  setConditions: (state, conditions) => (state.conditions = conditions),
  addCondition: (state, condition) => state.conditions.push(condition)
}

export const actions = {
  async fetchConditions({ commit }) {
    try {
      const URL = '/pipeline/condition'
      const res = await generic_get(this, URL)
      commit('setConditions', res)
      return res
    } catch (err) {
      console.log(err)
    }
  },
  async addCondition({ commit }, payload) {
    console.log(payload)
    try {
      const URL = '/pipeline/condition'
      const res = await generic_post(this, URL, {
        is_active: payload.isActive,
        condition_name: payload.conditionName,
        conditions: payload.conditions,
        pipeline: payload.pipeline
      })
      commit('addCondition', res)
    } catch (err) {
      console.log(err)
    }
  }
}
