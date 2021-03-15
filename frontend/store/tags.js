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
      console.log(err)
    }
  },
  async addTag({ commit }, data) {
    try {
      const URL = `/container/tags`
      const res = await generic_post(this, URL, data)
      console.log(res)
      console.log(state.tags)
      commit('addTag', res)
    } catch (err) {
      console.log(err)
    }
  },
  async addContainerTags({ commit }, data) {
    try {
      console.log('IN CONTAINER SEND ING SDKLJFHZSDL;FJL')
      console.log(data)
      const URL = `/container/${data.containerId}/tags`
      await generic_post(this, URL, data.tags)
    } catch (err) {
      console.log(err)
    }
  }
}
