import { getModalities, addModality } from '~/api/modalities'

export const state = () => ({
  modalities: []
})

export const mutations = {
  setModalities: (state, modalities) => (state.modalities = modalities),
  addModality: (state, modality) => (state.modalities.push(modality))
}

export const actions = {
  async fetchModalities({ commit }) {
    commit('setModalities', await getModalities(this))
  },
  async addModality({ commit }, modality) {
    commit('addModality', await addModality(this, modality))
  },
}
