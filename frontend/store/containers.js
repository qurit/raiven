import axios from 'axios'

export const state = () => ({
  containers: []
})

// TODO: UPDATE CONTAINER WITH MODAL FORM
export const mutations = {
  setContainers: (state, containers) => (state.containers = containers),
  addContainer: (state, container) => state.containers.push(container),
  deleteContainer: (state, container) =>
    state.containers.splice(state.containers.indexOf(container), 1)
}

export const actions = {
  async fetchContainers({ commit }) {
    const res = await axios.get('http://localhost:5000/container')
    commit('setContainers', res.data)
    console.log('got here')
    console.log(this.containers)
    console.log(res)
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
      commit('addContainer', data)
    } catch (err) {
      console.log(err)
    }
  }
}
