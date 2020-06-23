import { getModalities, addModality, deleteModality } from '~/api/modalities'

export const state = () => ({
  modalities: []
})

export const mutations = {
  setModalities: (state, modalities) => (state.modalities = modalities),
  addModality: (state, modality) => (state.modalities.push(modality)),
  removeModality: (state, { _id }) => state.modalities.filter(m => m._id !== _id),
}

export const actions = {
  async fetchModalities({ commit }) {
    commit('setModalities', await getModalities(this))
  },
  async addModality({ commit }, modality) {
    commit('addModality', await addModality(this, modality))
  },
  async deleteModality({ commit }, modality) {
    commit('removeModality', await deleteModality(this, modality))
  },
}
