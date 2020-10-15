import axios from 'axios'

export const state = () => ({
  dicomEvents: []
})

// TODO: UPDATE CONTAINER WITH MODAL FORM
export const mutations = {
  setDicomEvents: (state, dicomEvents) => (state.dicomEvents = dicomEvents)
}

export const actions = {
  async fetchDicomEvents({ commit }) {
    const res = await axios.get('http://localhost:5000/dicom/nodes')
    console.log(res.data)
    commit('setDicomEvents', res.data)
    return res.data
  }
}
