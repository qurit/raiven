import { generic_get, generic_post, generic_put } from '~/api'

export const state = () => ({
  users: []
})

export const mutations = {
  setUsers: (state, users) => (state.users = users),
  addUser: (state, user) => state.users.push(user),
  editUserSettings: (state, { id, res }) => {
    const index = state.users.findIndex(user => user.id === id)
    state.users[index].ae_title = res.ae_title
    state.users[index].access_allowed = res.access_allowed
    state.users[index].is_admin = res.is_admin
  }
}

export const actions = {
  async fetchUsers({ commit }) {
    try {
      const URL = '/user'
      const data = await generic_get(this, URL)
      data.forEach(user => {
        user.ldap_user ? (user['type'] = 'LDAP') : (user['type'] = 'LOCAL')
      })
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
  async editUserSettings(
    { commit },
    { id, ae_title, access_allowed, is_admin }
  ) {
    try {
      const URL = `/user/${id}`
      const res = await generic_put(this, URL, {
        ae_title: ae_title,
        access_allowed: access_allowed,
        is_admin: is_admin
      })
      commit('editUserSettings', { id, res })
      this.$toaster.toastSuccess('Settings updated!')
      return res
    } catch (err) {
      this.$toaster.toastError('Could not save changes.')
    }
  }
}
