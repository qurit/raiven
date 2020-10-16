import axios from 'axios'

export const state = () => ({
  destinations: []
})

// TODO: UPDATE CONTAINER WITH MODAL FORM
export const mutations = {
  setDestinations: (state, destinations) => (state.destinations = destinations),
  addDestination: (state, destination) => state.destinations.push(destination)
}

export const actions = {
  async fetchDestinations({ commit }) {
    try {
      const res = await axios.get('http://localhost:5000/destination')
      commit('setDestinations', res.data)
      console.log(res.data)
      return res.data
    } catch (err) {
      console.log(err)
    }
  },
  async addDestination({ commit }, data) {
    console.log(data)
    try {
      const res = await axios.post('http://localhost:5000/destination', {
        host: data.host,
        port: data.port
      })
      console.log(res)
      commit('addDestination', res.data)
    } catch (err) {
      console.log(err)
    }
  }
}
