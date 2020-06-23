import { getModalities } from '~/api/modalities'

export const state = () => ({
  modalities: []
})

export const mutations = {
  setModalities: (state, modalities) => (state.modalities = modalities)
}

export const actions = {
  async fetchModalities({ commit }) {
    commit('setModalities', await getModalities(this))
  },
}
