import { generic_get, generic_post } from '~/api'

export const state = () => ({
  tags: []
})

export const mutations = {
  setTags: (state, tags) => (state.tags = tags),
  addTag: (state, tag) => state.tags.push(tag)
}

export const actions = {
  async fetchTags({ commit }) {
    try {
      const URL = '/container/tags'
      const data = await generic_get(this, URL)
      commit('setTags', data)
      console.log(data)
      return data
    } catch (err) {
      console.log(err)
    }
  },
  async addTag({ commit }, container_id, data) {
    try {
      const URL = `/container/${container_id}/tags`
      const res = await generic_post(this, URL, data)
      commit('addTag', res)
    } catch (err) {
      console.log(err)
    }
  },
  async addContainerTags({ commit }, container_id, data) {
    try {
      const URL = `/container/${container_id}/tags`
      const res = await generic_post(this, URL, data)
      commit('addTag', res)
    } catch (err) {
      console.log(err)
    }
  }
}
