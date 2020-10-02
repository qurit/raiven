export const state = () => ({
  containers: [
    { id: 1, title: 'Input' },
    { id: 2, title: 'Anonymization' },
    { id: 3, title: 'Segmentation' },
    { id: 4, title: 'Output' }
  ]
})

export const mutations = {
  add: (state, container) => state.containers.push(container),
  delete: (state, container) => state.containers.splice(state.containers.indexOf(container), 1)
}
