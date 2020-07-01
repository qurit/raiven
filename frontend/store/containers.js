import { getContainers, scaleWorkers } from "../api/containers";

export const state = () => ({
  containers: []
})

export const getters = {
  workers: state => state.containers.filter(c => c.Config.Image === 'picom_worker')
}

export const mutations = {
  setContainers: (state, containers) => state.containers = containers,
}

export const actions = {
  async fetchContainers({commit}) {
      commit('setContainers', await getContainers(this))
  },
  async scaleWorkers({commit}, count) {
      await scaleWorkers(this, count)
      commit('setContainers', await getContainers(this))
  }
}
