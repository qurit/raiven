export const state = () => ({
  pipelines: [
    { id: 1, containerList: [{ id: 1, title: 'Algorithm 1' }] },
    { id: 2, containerList: [{ id: 1, title: 'Algorithm 6' }] }
  ]
})

export const mutations = {
  get(state) {
    state.pipelines
  },
  add(state, container) {
    state.pipelines.push(container)
  },
  delete(state, pipeline) {
    state.pipelines.splice(state.pipelines.indexOf(pipeline), 1)
  }
}
