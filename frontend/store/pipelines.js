export const state = () => ({
  pipelines: [
    {
      id: 1,
      title: 'Cool Pipeline',
      containerList: [{ id: 1, title: 'Algorithm 1' }],
      status: 80
    },
    {
      id: 2,
      title: 'Machine Learning Tumor Detection',
      containerList: [{ id: 1, title: 'Algorithm 6' }],
      status: 40
    }
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
