// old stuff

// import { getContainers, scaleWorkers } from "../api/containers";

// export const state = () => ({
//   containers: []
// })

// export const getters = {
//   workers: state => state.containers.filter(c => c.Name.startsWith('/picom_worker'))
// }

// export const mutations = {
//   setContainers: (state, containers) => state.containers = containers,
// }

// export const actions = {
//   async fetchContainers({commit}) {
//       commit('setContainers', await getContainers(this))
//   },
//   async scaleWorkers({commit}, count) {
//       await scaleWorkers(this, count)
//       commit('setContainers', await getContainers(this))
//   }
// }

export const state = () => ({
  containers: [
    { id: 1, title: 'Algorithm 1' },
    { id: 2, title: 'Algorithm 2' },
    { id: 3, title: 'Algorithm 3' }
  ]
})

export const mutations = {
  get(state) {
    state.containers
  }
}
