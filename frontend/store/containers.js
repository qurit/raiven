import axios from 'axios'

export const state = () => ({
  containers: []
})

// TODO: UPDATE CONTAINER WITH MODAL FORM
export const mutations = {
  setContainers: (state, containers) => (state.containers = containers),
  addContainer: (state, container) =>
    (state.containers = state.containers.concat(container)),
  deleteContainer: (state, id) => {
    const index = state.containers.findIndex(container => container.id === id)
    state.containers.splice(index, 1)
  },
  updateContainer: (state, { id, resultData }) => {
    const index = state.containers.findIndex(container => container.id === id)
    const container = state.containers[index]
    console.log(resultData)
    console.log(container)
    container.name = resultData.name
    container.description = resultData.description
    container.is_input_container = resultData.is_input_container
    container.is_output_container = resultData.is_output_container
    container.filename = resultData?.filename
    container.file = resultData?.file
  }
}

export const actions = {
  async fetchContainers({ commit }) {
    try {
      const res = await axios.get('http://localhost:5000/container')
      console.log(res)
      commit('setContainers', res.data)
      return res.data
    } catch (err) {
      console.log(err)
    }
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
      const res = await axios.post('http://localhost:5000/container', data)
      console.log(res)
      commit('addContainer', res.data)
    } catch (err) {
      console.log(err)
    }
  },
  async updateContainer({ commit }, payload) {
    try {
      const { id, data } = payload
      const res = await axios.put(`http://localhost:5000/container/${id}`, data)
      const resultData = res.data
      commit('updateContainer', { id, resultData })
    } catch (err) {
      console.log(err)
    }
  }
}
