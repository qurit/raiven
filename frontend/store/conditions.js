import { generic_get, generic_post, generic_delete } from '~/api'
const URL = '/pipeline/condition'

export const state = () => ({
  conditions: []
})

export const mutations = {
  setConditions: (state, conditions) => (state.conditions = conditions),
  addCondition: (state, condition) => state.conditions.push(condition),
  deleteCondition: (state, id) => {
    const index = state.conditions.findIndex(condition => condition.id === id)
    state.conditions.splice(index, 1)
  }
}

export const actions = {
  async fetchConditions({ commit }) {
    try {
      const res = await generic_get(this, URL)
      commit('setConditions', res)
      return res
    } catch (err) {
      console.log(err)
    }
  },
  async deleteCondition({ commit }, id) {
    try {
      await generic_delete(this, `${URL}/${id}`)
      commit('deleteCondition', id)
      this.$toaster.toastSuccess('Condition deleted!')
    } catch (err) {
      this.$toaster.toastError('Could not delete condition')
    }
  },
  async addCondition({ commit }, payload) {
    try {
      const res = await generic_post(this, URL, {
        condition_name: payload.conditionName,
        conditions: payload.conditions,
        pipeline: payload.pipeline
      })
      commit('addCondition', res)
      this.$toaster.toastSuccess('Condition added!')
    } catch (err) {
      this.$toaster.toastError('Could not add condition')
    }
  }
}
