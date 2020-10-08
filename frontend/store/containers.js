import axios from 'axios'

export const state = () => ({
  containers: []
})

// TODO: UPDATE CONTAINER WITH MODAL FORM
export const mutations = {
  setContainers: (state, containers) => (state.containers = containers),
  addContainer: (state, container) => state.containers.push(container),
  deleteContainer: (state, id) => {
    const index = state.containers.findIndex(container => container.id === id)
    state.containers.splice(index, 1)
  }
}

export const actions = {
  async fetchContainers({ commit }) {
    const res = await axios.get('http://localhost:5000/container')
    commit('setContainers', res.data)
    return res.data
  },
  async deleteContainer({ commit }, id) {
    try {
      await axios.delete(`http://localhost:5000/container/${id}`)
      commit('deleteContainer', id)
    } catch (err) {
      console.log(err)
    }
  },
  async addContainer({ commit }, data) {
    try {
      await axios.post('http://localhost:5000/container', data)
      const newContainer = {
        name: data.get('name'),
        description: data.get('description'),
        is_input_container: data.get('is_input_container'),
        is_output_container: data.get('is_output_container')
      }
      commit('addContainer', newContainer)
    } catch (err) {
      console.log(err)
    }
  }
}
