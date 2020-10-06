import axios from 'axios'

export const state = () => ({
  pipelines: []
})

export const mutations = {
  setPipelines: (state, pipelines) => (state.pipelines = pipelines),
  addPipeline: (state, pipeline) => state.pipelines.push(pipeline),
  deletePipeline: (state, pipeline) =>
    state.pipelines.splice(state.pipelines.indexOf(pipeline), 1)
}
export const actions = {
  async fetchPipelines({ commit }) {
    const res = await axios.get('http://localhost:5000/pipeline')
    commit('setPipelines', res.data)
    return res.data
  },
  async deletePipeline({ commit }, id) {
    try {
      await axios.delete(`http://localhost:5000/pipeline/${id}`)
      commit('deletePipeline', id)
    } catch (err) {
      console.log(err)
    }
  },
  async addPipeline({ commit }, data) {
    try {
      await axios.post('http://localhost:5000/pipeline', data)
      commit('addPipeline', data)
    } catch (err) {
      console.log(err)
    }
  }
}
