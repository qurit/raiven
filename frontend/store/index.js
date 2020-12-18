import { generic_get } from '~/api'

export const state = () => ({
    config: {
      PIPELINE_AE_PREFIX: 'RVP-',
      USER_AE_PREFIX: 'RVU-'
    }
})

export const mutations = {
    setConfig: (state, config) => state.config = config
}

export const actions = {
    async fetchConfig({commit}) {
        commit('setConfig', await generic_get(this, '/settings'))
    },
}
