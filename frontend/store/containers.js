import { generic_get, generic_post, generic_put, generic_delete } from '~/api'

export const state = () => ({
  containers: []
})

export const getters = {
  userContainers: (state, getters, rootState) => {
    return state.containers.filter(
      container => container.user_id === rootState.auth.user.id
    )
  },
  recentContainer: (state, getters, rootState) => {
    const max = state.containers.reduce(function(prev, current) {
      return prev.id > current.id ? prev : current
    })
    return max
  }
}

export const mutations = {
  setContainers: (state, containers) => (state.containers = containers),
  addContainer: (state, container) => state.containers.push(container),
  deleteContainer: (state, id) => {
    const index = state.containers.findIndex(container => container.id === id)
    state.containers.splice(index, 1)
  },
  updateContainer: (state, { id, res }) => {
    const index = state.containers.findIndex(container => container.id === id)
    const container = state.containers[index]
    container.name = res.name
    container.description = res.description
    container.is_input_container = res.is_input_container
    container.is_output_container = res.is_output_container
    container.is_shared = res.is_shared
    container.filename = res?.filename
    container.file = res?.file
  }
}

export const actions = {
  async fetchContainers({ commit }) {
    try {
      const URL = '/container'
      const data = await generic_get(this, URL)
      commit('setContainers', data)
      return data
    } catch (err) {
      console.log(err)
    }
  },
  async deleteContainer({ commit }, id) {
    try {
      const URL = `/container/${id}`
      await generic_delete(this, URL)
      commit('deleteContainer', id)
      this.$toaster.toastSuccess('Container Deleted Successfully')
    } catch (err) {
      this.$toaster.toastError('Container is Used in a Pipeline')
    }
  },
  async addContainer({ commit }, data) {
    try {
      const URL = '/container'
      const res = await generic_post(this, URL, data)
      commit('addContainer', res)
      return res
    } catch (err) {
      console.log(err)
    }
  },
  async updateContainer({ commit }, payload) {
    try {
      const { id, data } = payload
      const URL = `/container/${id}`
      const res = await generic_put(this, URL, data)
      commit('updateContainer', { id, res })
      return res
    } catch (err) {
      console.log(err)
    }
  }
}
