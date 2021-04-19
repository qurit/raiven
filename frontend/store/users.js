import { generic_get, generic_post, generic_put } from '~/api'

export const state = () => ({
  users: []
})

export const mutations = {
  setUsers: (state, users) => (state.users = users),
  addUser: (state, user) => state.users.push(user),
  editUserAETitle: (state, { id, res }) => {
    const index = state.users.findIndex(user => user.id === id)
    state.users[index].ae_title = res.ae_title
  },
  editAccess: (state, { id, res }) => {
    const index = state.users.findIndex(user => user.id === id)
    state.users[index].access_allowed = res.access_allowed
  },
  editRole: (state, { id, res }) => {
    const index = state.users.findIndex(user => user.id === id)
    state.users[index].is_admin = res.is_admin
  }
}

export const actions = {
  async fetchUsers({ commit }) {
    try {
      const URL = '/user'
      const data = await generic_get(this, URL)
      commit('setUsers', data)
      return data
    } catch (err) {
      this.$toaster.toastError('Could not fetch users')
    }
  },
  async addUser({ commit }, data) {
    try {
      const URL = `/user`
      const res = await generic_post(this, URL, data)
      commit('addUser', res)
      this.$toaster.toastSuccess('User added!')
    } catch (err) {
      this.$toaster.toastError('Could not add user')
    }
  },
  async editUserAETitle({ commit }, { id, ae_title }) {
    try {
      const URL = `/user/${id}`
      const res = await generic_put(this, URL, { ae_title: ae_title })
      commit('editUserAETitle', { id, res })
      this.$toaster.toastSuccess('AE Title updated!')
      return res
    } catch (err) {
      this.$toaster.toastError(
        'Could not save, make sure you have properly formed the AE title'
      )
    }
  },
  async changeAccess({ commit }, id) {
    try {
      const URL = `/user/modify-access/${id}`
      const res = await generic_put(this, URL)
      commit('editAccess', { id, res })
      this.$toaster.toastSuccess('User access changed!')
    } catch (err) {
      this.$toaster.toastError('Could not modify access')
    }
  },
  async changeRole({ commit }, id) {
    try {
      const URL = `/user/modify-role/${id}`
      const res = await generic_put(this, URL)
      commit('editRole', { id, res })
      this.$toaster.toastSuccess('User role changed!')
    } catch (err) {
      this.$toaster.toastError('Could not modify access')
    }
  }
}
