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
      const URL = '/dicom/nodes?output_node=true'
      const res = await generic_get(this, URL)
      commit('setDestinations', res)
      return res
    } catch (err) {
      console.log(err)
    }
  },
  async addDestination({ commit }, data) {
    try {
      const URL = '/destination'
      const res = await generic_post(this, URL, {
        host: data.host,
        port: data.port
      })
      commit('addDestination', res)
    } catch (err) {
      console.log(err)
    }
  }
}
