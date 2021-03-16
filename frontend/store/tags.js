import { generic_get, generic_post } from '~/api'

export const state = () => ({
  tags: []
})

export const mutations = {
  setTags: (state, tags) => (state.tags = tags),
  addTag: (state, tags) => (state.tags = state.tags.concat(tags))
}

export const actions = {
  async fetchTags({ commit }) {
    try {
      const URL = '/container/tags'
      const data = await generic_get(this, URL)
      commit('setTags', data)
      return data
    } catch (err) {
      this.$toaster.toastError('Could not fetch tags')
    }
  },
  async addTag({ commit }, data) {
    try {
      const URL = `/container/tags`
      const res = await generic_post(this, URL, data)
      commit('addTag', res)
    } catch (err) {
      this.$toaster.toastError('Could not add tags')
    }
  },
  async addContainerTags({ commit }, data) {
    try {
      const URL = `/container/${data.containerId}/tags`
      await generic_post(this, URL, data.tags)
    } catch (err) {
      this.$toaster.toastError('Could not associate Container tags')
    }
  }
}
