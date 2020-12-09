import { generic_get } from '~/api'

export const state = () => ({
    config: {}
})

export const mutations = {
    setConfig: (state, config) => state.settings = config,
}

export const actions = {
    async fetchConfig({commit}) {
        commit('setConfig', await generic_get(this, '/settings'))
    },
}
