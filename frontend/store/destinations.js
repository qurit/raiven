import axios from 'axios'

export const state = () => ({
  destinations: []
})

// TODO: UPDATE CONTAINER WITH MODAL FORM
export const mutations = {
  setDestinations: (state, destinations) => (state.destinations = destinations)
}

export const actions = {
  async fetchDestinations({ commit }) {
    try {
      const test = [
        { id: 1, host: '123', port: '1313', fullHostPort: '123 1313' },
        { id: 2, host: 'abc', port: 'sdfsdfsdf', fullHostPort: 'abc sdfsdfsdf' }
      ]
      commit('setDestinations', test)
      console.log('reached')
    } catch (err) {
      console.log(err)
    }
  }
}
