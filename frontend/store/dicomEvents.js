import { generic_get } from '~/api'

export const state = () => ({
  dicomEvents: []
})

// TODO: UPDATE CONTAINER WITH MODAL FORM
export const mutations = {
  setDicomEvents: (state, dicomEvents) => (state.dicomEvents = dicomEvents)
}

export const actions = {
  async fetchDicomEvents({ commit }) {
    try {
      const URL = '/dicom/nodes'
      const res = await generic_get(this, URL)
      commit('setDicomEvents', res)
      return res
    } catch (err) {
      console.log(err)
    }
  }
}
