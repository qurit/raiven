export const state = () => ({
  content: '',
  color: ''
})

export const mutations = {
  toastMessage (state, payload) {
    state.content = payload.content
    state.color = payload.color
  }
}
