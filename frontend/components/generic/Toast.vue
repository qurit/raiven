<template>
  <v-snackbar v-model="show" :color="color" :timeout="2000" right top style="z-index: 10000">
    {{ message }}
    <template v-slot:action><v-btn text @click="show = false">Close</v-btn></template>
  </v-snackbar>
</template>

<script>
export default {
  name: 'Toast',
  data () {
    return {
      show: false,
      message: '',
      color: ''
    }
  },
  created () {
    this.$store.subscribe((mutation, state) => {
      if (mutation.type === 'toast/toastMessage') {
        this.message = state.toast.content
        this.color = state.toast.color
        this.show = true
      }
    })
  }
}
</script>

<style scoped>

</style>
