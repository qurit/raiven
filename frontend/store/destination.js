import { generic_get, generic_post } from '~/api'

export const state = () => ({
  destinations: []
})

export const mutations = {
  setDestinations: (state, destinations) => (state.destinations = destinations),
  addDestination: (state, destination) => state.destinations.push(destination)
}

export const actions = {
  async fetchDestinations({ commit }) {
    try {
      const URL = '/dicom/nodes?output_node=true&rts=true'
      const res = await generic_get(this, URL)
      commit('setDestinations', res)
      return res
    } catch (err) {
      console.log(err)
    }
  },
  async addDestination({ commit }, node) {
    try {
      const URL = '/dicom/nodes'
      const res = await generic_post(this, URL, node)

      commit('addDestination', res)
    } catch (e) {
      let msg = 'Node Exists Already'
      try {
        msg = e.response.data.detail
      } finally {
        this.$toaster.toastError(msg)
      }
    }
  }
}
