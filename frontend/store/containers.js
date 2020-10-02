export const state = () => ({
  containers: [
    { id: 1, title: 'Algorithm 1' },
    { id: 2, title: 'Algorithm 2' },
    { id: 3, title: 'Algorithm 3' }
  ]
})

export const mutations = {
  add: (state, container) => state.containers.push(container),
  delete: (state, container) => state.containers.splice(state.containers.indexOf(container), 1)
}
