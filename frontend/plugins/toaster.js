export default ({ app, store }, inject) => {
  inject('toaster', {
    toastMessage ({ content = '', color = '' }) {
      store.commit('toast/toastMessage', { content, color })
    },
    toastError(msg = 'Error') {
      this.toastMessage({ content: msg, color: 'error'})
    },
    toastSuccess(msg = 'Success') {
       this.toastMessage({ content: msg, color: 'success'})
    },
  })
}
